import asyncio

import os
from instagrapi import Client
from database import db
from config import LOGIN_INST, PASSWORD_INST

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

SESSION_PATH = os.path.join(CURRENT_DIR, "session.json")

cl = Client()

cl.request_timeout = 20

async def process_scanner(all_accounts, max_taken):
    if os.path.exists(SESSION_PATH):
        await asyncio.to_thread(cl.load_settings, SESSION_PATH)
    else:
        await asyncio.to_thread(cl.login, LOGIN_INST, PASSWORD_INST)
        await asyncio.to_thread(cl.dump_settings, SESSION_PATH)
    
    for i, account in enumerate(all_accounts):
        all_accounts[i]['new_shortcodes'] = set()
        
        try:

            user_id = await asyncio.to_thread(cl.user_id_from_username, account['name'])

            medias = await asyncio.to_thread(cl.user_medias, user_id=user_id, amount=max_taken)
            
            medias = medias[::-1]

            for media in medias:
                if media.code not in account['shortcodes']:
                    hashtags = [tag for tag in media.caption_text.split() if tag.startswith("#")]
                    await db.add_post(
                        account_id=account['id'],
                        shortcode=media.code,
                        media_type=media.media_type,
                        caption=media.caption_text,
                        hashtags=hashtags,
                        status='pending'
                    )
        except Exception as e:
            print(f"Error scanning {account['name']}: {e}")
    