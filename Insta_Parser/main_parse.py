from database import db
from config import MAX_TAKEN, LIMIT_POSTS
from Insta_Parser.scanner import process_scanner
from Insta_Parser.worker import process_worker

async def main_process(app):
    all_accounts = await db.get_accounts()
    
    for i, account in enumerate(all_accounts):
        shortcodes = await db.get_shortcodes(account_id=account['id'], max_taken=MAX_TAKEN)
        all_accounts[i]['shortcodes'] = shortcodes

    #await process_scanner(all_accounts=all_accounts, max_taken=MAX_TAKEN)

    await process_worker(app, LIMIT_POSTS)
