import asyncio
import random
import os
from instagrapi import Client
from database import db
from config import LOGIN_INST, PASSWORD_INST

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

SESSION_PATH = os.path.join(CURRENT_DIR, "session.json")

cl = Client()

cl.request_timeout = 60

async def process_scanner(all_accounts, max_taken):
    if os.path.exists(SESSION_PATH):
        await asyncio.to_thread(cl.load_settings, SESSION_PATH)
        print(f"[AUTH] Найдена сессия {SESSION_PATH}, загружаем...")
    else:
        print(f"[AUTH] Сессия не найдена, входим по логину {LOGIN_INST}...")
        await asyncio.to_thread(cl.login, LOGIN_INST, PASSWORD_INST)
        await asyncio.to_thread(cl.dump_settings, SESSION_PATH)
        print(f"[AUTH] Новый файл сессии сохранен.")
    
    print("[SCAN] Начинаю обход аккаунтов...")
    for i, account in enumerate(all_accounts):
        all_accounts[i]['new_shortcodes'] = set()
        insta_id = account['insta_id']

        try:
            wait_time = random.uniform(30, 60)
            print(f"[SCAN] Пауза {wait_time:.1f} сек. перед {account['name']}...")
            await asyncio.sleep(wait_time)

            print(f"[SCAN] Работаю с аккаунтом: {account['name']}")

            if not insta_id:
                print(f"[SCAN] ID для {account['name']} не найден в базе, запрашиваю...")
                insta_id= await asyncio.to_thread(cl.user_id_from_username, account['name'])
                await db.add_insta_id(account_id=account['id'], insta_id=insta_id)
                wait_time = random.uniform(30, 60)
                print(f"[SCAN] Пауза {wait_time:.1f} сек.")
                await asyncio.sleep(wait_time)
            
            print(f"[SCAN] ID подтвержден: {insta_id}. Приступаю к получению фида и диагностике контента...")
            medias_feed = await asyncio.to_thread(cl.user_medias, user_id=str(insta_id), amount=max_taken)
            print(f"[FEED]  @{account['name']}: получено {len(medias_feed)} постов из основной ленты")

            wait_time = random.uniform(30, 60)
            print(f"[SCAN] Пауза {wait_time:.1f} сек.")
            await asyncio.sleep(wait_time)
            medias_reels = await asyncio.to_thread(cl.user_clips, user_id=str(insta_id), amount=max_taken)
            print(f"[REELS] @{account['name']}: получено {len(medias_reels)} роликов из вкладки Reels")

            # Объединяем
            all_media_objects = {m.code: m for m in (medias_feed + medias_reels)}.values()
            medias = sorted(all_media_objects, key=lambda x: x.taken_at)
            
            print(f"[MERGE] @{account['name']}: после объединения всего {len(medias)} уникальных медиа")

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
                    print(f"  [+] Добавлен новый пост: {media.code}")
        except Exception as e:
            print(f"Error scanning {account['name']}: {e}")
        
        print("[SCAN] Цикл сканирования завершен. Все аккаунты проверены.")
    