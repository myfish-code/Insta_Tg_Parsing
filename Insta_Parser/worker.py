import asyncio
import random
import os
import shutil
from pyrogram.types import InputMediaPhoto, InputMediaVideo
import subprocess
import json
from config import CHANNEL_ID
from database import db
from yt_dlp import YoutubeDL
import glob

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOADS_FOLDER = os.path.join(CURRENT_DIR, "downloads")

os.makedirs(DOWNLOADS_FOLDER, exist_ok=True)

def sync_download_ytdlp(url, shortcode, output_folder):
    # Упрощаем шаблон: файлы будут называться shortcode_1.mp4, shortcode_2.jpg и т.д.
    output_template = os.path.join(output_folder, f"{shortcode}_%(playlist_index)s.%(ext)s")
    
    ydl_opts = {
        'outtmpl': output_template,
        'timeout': 60,
        'overwrites': True,
        'cookiefile': os.path.join(CURRENT_DIR, "cookies.txt"),  # Подсовываем куки
        'quiet': True,
        'no_warnings': False, 
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
    print("[WORKER] Проверка канала...")
    await app.get_chat(CHANNEL_ID)

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
            print(f"  [>] Запуск скачивания через yt-dlp...")
            await asyncio.to_thread(sync_download_ytdlp, full_link, shortcode, DOWNLOADS_FOLDER)

            downloaded_files = sorted(glob.glob(os.path.join(DOWNLOADS_FOLDER, f"{shortcode}*")))
            if not downloaded_files:
                raise Exception(f"yt-dlp завершился, но файлы с префиксом {shortcode} не найдены.")
            
            # --- ТИП 1: ОДИНОЧНОЕ ФОТО ---
            if media_type == 1:
                file_path = downloaded_files[0]
                await app.send_photo(chat_id=CHANNEL_ID, photo=str(file_path), caption=final_caption)
                
            # --- ТИП 2: REELS / ВИДЕО ---
            elif media_type == 2:
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

            # --- ТИП 8: КАРУСЕЛЬ (АЛЬБОМ) ---
            elif media_type == 8:
                media_group = []
                if len(downloaded_files) > 10:
                    downloaded_files = downloaded_files[:10]

                for i, p_str in enumerate(downloaded_files):
                    curr_cap = final_caption if i == 0 else "" 
                    p_lower = p_str.lower()

                    if p_lower.endswith(('.mp4', '.mov', '.m4v', '.webm')):
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

                # ТУТ ПОПРАВИЛ ОТСТУПЫ: отправка идет строго после сборки цикла
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