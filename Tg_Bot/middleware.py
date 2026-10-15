from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from typing import Callable, Dict, Any, Awaitable
from config import ADMINS

class BanCheckMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message | CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        
        telegram_id = event.from_user.id if event.from_user else None
        if not telegram_id:
            return await handler(event, data)

        if telegram_id not in ADMINS:
            if isinstance(event, Message):
                await event.answer("🚫 Доступ ограничен.")
            elif isinstance(event, CallbackQuery):
                await event.answer("🚫 Доступ ограничен.", show_alert=True)
            return

        return await handler(event, data)