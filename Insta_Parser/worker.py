import asyncio
import random
import os
import shutil
from pyrogram.types import InputMediaPhoto, InputMediaVideo
import subprocess
import json
from instagrapi import Client
from config import CHANNEL_ID, LOGIN_INST, PASSWORD_INST
from database import db
from yt_dlp import YoutubeDL
import glob

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOADS_FOLDER = os.path.join(CURRENT_DIR, "downloads")
SESSION_PATH = os.path.join(CURRENT_DIR, "session.json")

os.makedirs(DOWNLOADS_FOLDER, exist_ok=True)

cl = Client()
cl.request_timeout = 90

def sync_download_ytdlp(url, shortcode, output_folder):
    output_template = os.path.join(output_folder, f"{shortcode}%(autonumber, -| )s.%(ext)s")
    
    ydl_opts = {
        'outtmpl': output_template,
        'timeout': 60,
        'overwrites': True,
        'quiet': True,
        'no_warnings': True,
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
    print("[WORKER] Проверка канала и авторизация в Instagram...")
    await app.get_chat(CHANNEL_ID)

    # Возвращаем авторизацию instagrapi для фото и альбомов
    if os.path.exists(SESSION_PATH):
        await asyncio.to_thread(cl.load_settings, SESSION_PATH)
    else:
        await asyncio.to_thread(cl.login, LOGIN_INST, PASSWORD_INST)
        await asyncio.to_thread(cl.dump_settings, SESSION_PATH)

    pending_posts = await db.get_pending_posts(limit=limit)
    print(f"[WORKER] Найдено постов в очереди: {len(pending_posts)}")

    phrase = await db.get_phrase()

    for pending_post in pending_posts:
        shortcode = pending_post['shortcode']
        media_type = pending_post['media_type']
        caption = pending_post['caption']

        print(f"[WORKER] Обработка поста: {shortcode} (Type: {media_type})")

        if phrase:
            final_caption = f"{caption}\n\n{phrase}"
        else:
            final_caption = caption

        type_link = "reels" if media_type == 2 else "p"
        full_link = f"https://www.instagram.com/{type_link}/{shortcode}/"

        try:
            # --- ТИП 1: ОДИНОЧНОЕ ФОТО (Через instagrapi) ---
            if media_type == 1:
                print(f"  [>] Скачивание фото через instagrapi...")
                media_pk = await asyncio.to_thread(cl.media_pk_from_url, full_link)
                file_path = await asyncio.to_thread(cl.photo_download, media_pk, folder=DOWNLOADS_FOLDER)
                await app.send_photo(chat_id=CHANNEL_ID, photo=str(file_path), caption=final_caption)
                
            # --- ТИП 2: REELS / ВИДЕО (Через yt-dlp) ---
            elif media_type == 2:
                print(f"  [>] Запуск скачивания Reels через yt-dlp...")
                await asyncio.to_thread(sync_download_ytdlp, full_link, shortcode, DOWNLOADS_FOLDER)

                downloaded_files = sorted(glob.glob(os.path.join(DOWNLOADS_FOLDER, f"{shortcode}*")))
                if not downloaded_files:
                    raise Exception(f"yt-dlp завершился, но файлы с префиксом {shortcode} не найдены.")
                
                file_path = downloaded_files[0]
                width, height = await get_video_dims(file_path)
                await app.send_video(
                    chat_id=CHANNEL_ID,
                    video=str(file_path),
                    width=width,
                    height=height,
                    supports_streaming=True,
                    caption=final_caption
                )

            # --- ТИП 8: КАРУСЕЛЬ (АЛЬБОМ) (Через instagrapi) ---
            elif media_type == 8:
                print(f"  [>] Скачивание альбома через instagrapi...")
                media_pk = await asyncio.to_thread(cl.media_pk_from_url, full_link)
                media_group = []
                file_path = await asyncio.to_thread(cl.album_download, media_pk, folder=DOWNLOADS_FOLDER)

                if len(file_path) > 10:
                    file_path = file_path[:10]

                for i, p in enumerate(file_path):
                    p_str = str(p) 
                    curr_cap = final_caption if i == 0 else "" 
                    p_lower = p_str.lower()

                    if p_lower.endswith(('.mp4', '.mov', '.m4v')):
                        w, h = await get_video_dims(p_str)
                        media_group.append(
                            InputMediaVideo(
                                p_str, 
                                caption=curr_cap,
                                width=w,
                                height=h,
                                supports_streaming=True
                            )
                        )
                    else: 
                        media_group.append(InputMediaPhoto(p_str, caption=curr_cap))

                try:
                    await app.send_media_group(chat_id=CHANNEL_ID, media=media_group)
                except Exception as e:
                    if "MEDIA_EMPTY" in str(e):
                        media_group = [m for m in media_group if isinstance(m, InputMediaPhoto)]
                        if media_group:
                            media_group[0].caption = final_caption
                            await app.send_media_group(chat_id=CHANNEL_ID, media=media_group)

            await db.update_status_post(pending_post['id'], 'completed')
            print(f"  [OK] Пост {shortcode} успешно отправлен!")

            wait_time = random.randint(60, 120)
            print(f"[WORKER] Ожидание {wait_time} сек. перед следующим постом...")
            await asyncio.sleep(wait_time)

        except Exception as e:
            print(f"Error worker : {e}")
            await db.update_status_post(pending_post['id'], 'error')
        
        finally:
            if os.path.exists(DOWNLOADS_FOLDER):
                shutil.rmtree(DOWNLOADS_FOLDER)
                os.makedirs(DOWNLOADS_FOLDER, exist_ok=True)

    print("[WORKER] Все задачи выполнены.")