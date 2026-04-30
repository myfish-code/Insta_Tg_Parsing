import asyncio

import os
import shutil
from instagrapi import Client
from pyrogram.types import InputMediaPhoto, InputMediaVideo

from config import CHANNEL_ID, LOGIN_INST, PASSWORD_INST
from database import db

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

DOWNLOADS_FOLDER = os.path.join(CURRENT_DIR, "downloads")
SESSION_PATH = os.path.join(CURRENT_DIR, "session.json")

os.makedirs(DOWNLOADS_FOLDER, exist_ok=True)

cl = Client()

cl.request_timeout = 20

async def process_worker(app, limit):
    if os.path.exists(SESSION_PATH):
        await asyncio.to_thread(cl.load_settings, SESSION_PATH)
    else:
        await asyncio.to_thread(cl.login, LOGIN_INST, PASSWORD_INST)
        await asyncio.to_thread(cl.dump_settings, SESSION_PATH)

    pending_posts = await db.get_pending_posts(limit=limit)
    
    for pending_post in pending_posts:
        shortcode = pending_post['shortcode']
        media_type = pending_post['media_type']
        caption = pending_post['caption']

        type_link = "reels" if media_type == 2 else "p"
        full_link = f"https://www.instagram.com/{type_link}/{shortcode}/"

        media_pk = await asyncio.to_thread(cl.media_pk_from_url, full_link)

        try:
            if media_type == 1:
                file_path = await asyncio.to_thread(cl.photo_download, media_pk, folder=DOWNLOADS_FOLDER)
                await app.send_photo(chat_id=CHANNEL_ID, photo=str(file_path), caption=caption)

            elif media_type == 2:
                file_path = await asyncio.to_thread(cl.video_download, media_pk, folder=DOWNLOADS_FOLDER)
                await app.send_video(chat_id=CHANNEL_ID, video=str(file_path), caption=caption)

            elif media_type == 8:
                file_path = await asyncio.to_thread(cl.album_download, media_pk, folder=DOWNLOADS_FOLDER)
                media_group = []

                if len(file_path) > 10:
                    file_path = file_path[:10]

                for i, p in enumerate(file_path):
                    p_str = str(p) 
                    curr_cap = caption if i == 0 else "" 
                    
                    if p_str.lower().endswith(('.mp4', '.mov')):
                        media_group.append(InputMediaVideo(p_str, caption=curr_cap))
                    else: 
                        media_group.append(InputMediaPhoto(p_str, caption=curr_cap))
                    
                await app.send_media_group(chat_id=CHANNEL_ID, media=media_group)

            await db.update_status_post(pending_post['id'], 'completed')

        except Exception as e:
            print(f"Error worker : {e}")
            await db.update_status_post(pending_post['id'], 'error')
        
        finally:
            if os.path.exists(DOWNLOADS_FOLDER):
                shutil.rmtree(DOWNLOADS_FOLDER)
                os.makedirs(DOWNLOADS_FOLDER, exist_ok=True)