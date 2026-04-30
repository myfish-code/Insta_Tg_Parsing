import math

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

async def start_usage_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📱 Мої аккаунти", callback_data="my_accounts")],
    ])

    return keyboard

async def back_to_home():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏠 Головне меню", callback_data="back_to_main")]
    ])

    return keyboard

async def back_to_main_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Додати новий акаунт", callback_data="add_account")],
        [InlineKeyboardButton(text="🏠 Головне меню", callback_data="back_to_main")]
    ])

    return keyboard

async def after_add_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Додати новий акаунт", callback_data="add_account")],
        [InlineKeyboardButton(text="📱 Мої аккаунти", callback_data="my_accounts")],
        [InlineKeyboardButton(text="🏠 Головне меню", callback_data="back_to_main")]
    ])

    return keyboard

async def after_making_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📱 Мої аккаунти", callback_data="my_accounts")],
        [InlineKeyboardButton(text="🏠 Головне меню", callback_data="back_to_main")]
    ])

    return keyboard

async def pagination_keyboard(current_page, page_size, all_name):
    total_pages = math.ceil(len(all_name) / page_size)
    
    text = f"📋 **Ваші акаунти ({current_page}/{total_pages}):**\n\n"

    min_page = max(current_page - 1, 1)
    max_page = min(current_page + 1, total_pages)

    callback_min_page = f"page:{min_page}" if min_page < current_page else "no_action_left"
    callback_max_page = f"page:{max_page}" if max_page > current_page else "no_action_right"

    account_buttons = []

    first_elem = (current_page - 1) * page_size + 1
    last_elem = min(first_elem + 4, len(all_name))
    for elem in range(first_elem, last_elem + 1):
        account_buttons.append(
            InlineKeyboardButton(text=f"{elem}", callback_data=f"element:{all_name[elem - 1]['id']}")
        )

        text += f"{elem}. `{all_name[elem - 1]['name']}`\n"
    
    text += "\nОберіть номер для керування:"

    pagination_buttons = [
        InlineKeyboardButton(text="◀️ Назад", callback_data=callback_min_page),
        InlineKeyboardButton(text=f"📃 {current_page}/{total_pages}", callback_data="no_action_current"),
        InlineKeyboardButton(text="▶️ Вперед", callback_data=callback_max_page)
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
            account_buttons,
            pagination_buttons,
            [InlineKeyboardButton(text="➕ Додати новий акаунт", callback_data="add_account")],
            [InlineKeyboardButton(text="🏠 Головне меню", callback_data="back_to_main")]
        ])

    return (text, keyboard)


async def not_found_account_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📱 Мої аккаунти", callback_data="my_accounts")],
        [InlineKeyboardButton(text="🏠 Головне меню", callback_data="back_to_main")]
    ])

    return keyboard

async def change_account_keyboard(id):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✏️ Редагувати назву", callback_data=f"refactor:{id}")],
        [InlineKeyboardButton(text="🗑 Видалити", callback_data=f"delete:{id}")],
        [InlineKeyboardButton(text="📱 Мої аккаунти", callback_data="my_accounts")],
        [InlineKeyboardButton(text="🏠 Головне меню", callback_data="back_to_main")]
    ])

    return keyboard

async def after_refactor_keyboard(id):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✏️ Змінити ще раз", callback_data=f"refactor:{id}")],
        [InlineKeyboardButton(text="📱 Мої аккаунти", callback_data="my_accounts")],
        [InlineKeyboardButton(text="🏠 Головне меню", callback_data="back_to_main")]
    ])

    return keyboard