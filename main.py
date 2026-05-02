from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
from datetime import datetime
from pyrogram import Client
import os

from config import BOT_TOKEN, API_HASH, API_ID, CHANNEL_LINK
from database import db
from Tg_Bot.handlers import router
from Insta_Parser.main_parse import main_process

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
session_path = os.path.join(BASE_DIR, "Insta_Parser", "my_session")

async def main():
    await db.init_pool()
    
    app = Client(session_path, api_id=API_ID, api_hash=API_HASH, no_updates=True)

    await app.start()
    
    chat = await app.get_chat(CHANNEL_LINK)

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    
    dp.include_router(router)

    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        main_process, 
        "interval", 
        minutes=60,
        jitter=1800,
        id="insta_parser_job",
        next_run_time=datetime.now(),
        max_instances=1,
        kwargs={"app": app}
    )

    scheduler.start()

    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass