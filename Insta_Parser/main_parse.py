import asyncio
import random
from database import db
from config import MAX_TAKEN, LIMIT_POSTS
from Insta_Parser.scanner import process_scanner
from Insta_Parser.worker import process_worker

async def main_process(app):
    all_accounts = await db.get_accounts()
    
    for i, account in enumerate(all_accounts):
        shortcodes = await db.get_shortcodes(account_id=account['id'])
        all_accounts[i]['shortcodes'] = shortcodes

    await process_scanner(all_accounts=all_accounts, max_taken=MAX_TAKEN)

    wait_time = random.uniform(100, 200)
    await asyncio.sleep(wait_time)
    print(f"[SCAN] Пауза {wait_time:.1f} сек.")

    await process_worker(app, LIMIT_POSTS)
