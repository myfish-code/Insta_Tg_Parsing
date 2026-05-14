import asyncio
import random
from database import db
from config import MAX_TAKEN, LIMIT_POSTS
from Insta_Parser.scanner import process_scanner
from Insta_Parser.worker import process_worker

async def main_process(app):
    pending_count = await db.get_pending_count()

    if pending_count > 0:
        print(f"[SKIP] В очереди еще {pending_count} постов. Пропускаем сканирование, чтобы не спамить.")
    else:

        all_accounts = await db.get_accounts()
    
        for i, account in enumerate(all_accounts):
            shortcodes = await db.get_shortcodes(account_id=account['id'])
            all_accounts[i]['shortcodes'] = shortcodes

        await process_scanner(all_accounts=all_accounts, max_taken=MAX_TAKEN)

    wait_time = random.uniform(100, 200)
    print(f"[SCAN] Пауза {wait_time:.1f} сек.")
    await asyncio.sleep(wait_time)

    await process_worker(app, LIMIT_POSTS)
