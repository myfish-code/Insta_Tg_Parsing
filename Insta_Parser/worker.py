import asyncio
import random
import os
import shutil
from instagrapi import Client
from pyrogram.types import InputMediaPhoto, InputMediaVideo
import subprocess
import json
from config import CHANNEL_ID, LOGIN_INST, PASSWORD_INST
from database import db

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

DOWNLOADS_FOLDER = os.path.join(CURRENT_DIR, "downloads")
SESSION_PATH = os.path.join(CURRENT_DIR, "session.json")

os.makedirs(DOWNLOADS_FOLDER, exist_ok=True)

cl = Client()

cl.request_timeout = 20


async def get_video_dims(path):
    # Команда вытаскивает только ширину и высоту в формате JSON
    cmd = [
        'ffprobe', '-v', 'error', '-select_streams', 'v:0',
        '-show_entries', 'stream=width,height', '-of', 'json', path
    ]
    # Запускаем в отдельном потоке, чтобы не вешать асинхронность
    result = await asyncio.to_thread(subprocess.check_output, cmd)
    data = json.loads(result)
    return data['streams'][0]['width'], data['streams'][0]['height']

async def process_worker(app, limit):
    print("[WORKER] Проверка канала и авторизация...")
    await app.get_chat(CHANNEL_ID)

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
            print(f"  [>] Скачивание медиа...")
            media_pk = await asyncio.to_thread(cl.media_pk_from_url, full_link)

            if media_type == 1:
                file_path = await asyncio.to_thread(cl.photo_download, media_pk, folder=DOWNLOADS_FOLDER)
                await app.send_photo(chat_id=CHANNEL_ID, photo=str(file_path), caption=final_caption)
                
            elif media_type == 2:
                file_path = await asyncio.to_thread(cl.video_download, media_pk, folder=DOWNLOADS_FOLDER)
                width, height = await get_video_dims(file_path)
                await app.send_video(
                    chat_id=CHANNEL_ID,
                    video=str(file_path),
                    width=width,               # Явно задаем ширину
                    height=height,             # Явно задаем высоту
                    supports_streaming=True,    # КРИТИЧНО для iPhone!
                    caption=final_caption
                )

            elif media_type == 8:
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
                                width=w,                # Явно задаем ширину
                                height=h,               # Явно задаем высоту
                                supports_streaming=True # Чтобы видео в альбоме открывалось плавно
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