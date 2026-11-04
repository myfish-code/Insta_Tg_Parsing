import asyncio
import random
import os
import shutil
from pyrogram.types import InputMediaPhoto, InputMediaVideo
import subprocess
import json
from instagrapi import Client
from config import CHANNEL_ID, LOGIN_INST, PASSWORD_INST, PROXY_URL
from database import db
from yt_dlp import YoutubeDL
import glob

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOADS_FOLDER = os.path.join(CURRENT_DIR, "downloads")
SESSION_PATH = os.path.join(CURRENT_DIR, "session.json")

os.makedirs(DOWNLOADS_FOLDER, exist_ok=True)

cl = Client()
cl.set_proxy(PROXY_URL)

cl.request_timeout = 90

def sync_download_ytdlp(url, shortcode, output_folder):
    output_template = os.path.join(output_folder, f"{shortcode}.%(ext)s")
    
    ydl_opts = {
        'outtmpl': output_template,
        'timeout': 60,
        'overwrites': True,
        'quiet': True,
        'no_warnings': True,
        'ignoreerrors': False,  
    }
    
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
async def get_video_dims(path):
    cmd = [
        'ffprobe', '-v', 'error', '-select_streams', 'v:0',
        '-show_entries', 'stream=width,height', '-of', 'json', path
    ]
    result = await asyncio.to_thread(subprocess.check_output, cmd)
    data = json.loads(result)
    return data['streams'][0]['width'], data['streams'][0]['height']

async def process_worker(app, limit):
    print("[WORKER] Проверка канала и авторизация в Instagram...", flush=True)
    await app.get_chat(CHANNEL_ID)

    if os.path.exists(SESSION_PATH):
        await asyncio.to_thread(cl.load_settings, SESSION_PATH)
    else:
        await asyncio.to_thread(cl.login, LOGIN_INST, PASSWORD_INST)
        await asyncio.to_thread(cl.dump_settings, SESSION_PATH)

    pending_posts = await db.get_pending_posts(limit=limit)
    print(f"[WORKER] Найдено постов в очереди: {len(pending_posts)}", flush=True)

    phrase = await db.get_phrase()

    for pending_post in pending_posts:
        shortcode = pending_post['shortcode']
        media_type = pending_post['media_type']
        caption = pending_post['caption']

        print(f"[WORKER] Обработка поста: {shortcode} (Type: {media_type})", flush=True)

        final_caption = f"{caption}\n\n{phrase}" if phrase else caption
        type_link = "reels" if media_type == 2 else "p"
        full_link = f"https://www.instagram.com/{type_link}/{shortcode}/"

        try:
            # --- ТИП 1: ОДИНОЧНОЕ ФОТО ---
            if media_type == 1:
                print(f"  [>] Скачивание фото через instagrapi...", flush=True)
                media_pk = await asyncio.to_thread(cl.media_pk_from_url, full_link)
                file_path = await asyncio.to_thread(cl.photo_download, media_pk, folder=DOWNLOADS_FOLDER)
                await app.send_photo(chat_id=CHANNEL_ID, photo=str(file_path), caption=final_caption)

            # --- ТИП 2: REELS / ВИДЕО ---
            elif media_type == 2:
                print(f"  [>] Запуск скачивания Reels через yt-dlp...", flush=True)
                
                if os.path.exists(DOWNLOADS_FOLDER):
                    shutil.rmtree(DOWNLOADS_FOLDER)
                os.makedirs(DOWNLOADS_FOLDER, exist_ok=True)

                await asyncio.to_thread(sync_download_ytdlp, full_link, shortcode, DOWNLOADS_FOLDER)

                downloaded_files = sorted(glob.glob(os.path.join(DOWNLOADS_FOLDER, "*")))
                if not downloaded_files:
                    raise Exception(f"yt-dlp не смог скачать файл для {shortcode}")

                file_path = downloaded_files[0]

                try:
                    w, h = await get_video_dims(file_path)
                    width, height = int(w), int(h)
                except Exception:
                    width, height = None, None

                send_kwargs = {
                    "chat_id": CHANNEL_ID,
                    "video": str(file_path),
                    "supports_streaming": True,
                    "caption": final_caption
                }
                if width and height:
                    send_kwargs["width"] = width
                    send_kwargs["height"] = height

                await app.send_video(**send_kwargs)

            # --- ТИП 8: КАРУСЕЛЬ (АЛЬБОМ) ---
            elif media_type == 8:
                print(f"  [>] Скачивание альбома через instagrapi...", flush=True)
                media_pk = await asyncio.to_thread(cl.media_pk_from_url, full_link)
                
                try:
                    file_path = await asyncio.to_thread(cl.album_download, media_pk, folder=DOWNLOADS_FOLDER)
                except Exception as album_err:
                    print(f"  [!] Дефолтный метод альбома упал ({album_err}). Переходим на media_info...", flush=True)
                    info = await asyncio.to_thread(cl.media_info, media_pk)
                    file_path = []
                    for item in info.resources:
                        if item.media_type == 1:
                            res_path = await asyncio.to_thread(cl.photo_download_by_url, item.thumbnail_url, folder=DOWNLOADS_FOLDER)
                            if res_path: file_path.append(res_path)
                        elif item.media_type == 2:
                            res_path = await asyncio.to_thread(cl.video_download_by_url, item.video_url, folder=DOWNLOADS_FOLDER)
                            if res_path: file_path.append(res_path)

                if len(file_path) > 10:
                    file_path = file_path[:10]

                media_group = []
                for i, p in enumerate(file_path):
                    p_str = str(p) 
                    curr_cap = final_caption if i == 0 else "" 
                    p_lower = p_str.lower()

                    if p_lower.endswith(('.mp4', '.mov', '.m4v')):
                        try:
                            w, h = await get_video_dims(p_str)
                            media_group.append(InputMediaVideo(p_str, caption=curr_cap, width=int(w), height=int(h), supports_streaming=True))
                        except Exception:
                            media_group.append(InputMediaVideo(p_str, caption=curr_cap, supports_streaming=True))
                    else: 
                        media_group.append(InputMediaPhoto(p_str, caption=curr_cap))

                if media_group:
                    await app.send_media_group(chat_id=CHANNEL_ID, media=media_group)

            # Отмечаем статус как completed ТОЛЬКО если пост отправлен
            await db.update_status_post(pending_post['id'], 'completed')
            print(f"  [OK] Пост {shortcode} успешно отправлен!", flush=True)

            wait_time = random.randint(60, 120)
            print(f"[WORKER] Ожидание {wait_time} сек. перед следующим постом...", flush=True)
            await asyncio.sleep(wait_time)

        except Exception as e:
            import traceback
            print(f"  [!] Ошибка при обработке {shortcode}: {e}", flush=True)
            traceback.print_exc()
            await db.update_status_post(pending_post['id'], 'error')
        
        finally:
            if os.path.exists(DOWNLOADS_FOLDER):
                shutil.rmtree(DOWNLOADS_FOLDER)
                os.makedirs(DOWNLOADS_FOLDER, exist_ok=True)

    print("[WORKER] Все задачи выполнены.", flush=True)