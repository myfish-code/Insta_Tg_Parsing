from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from Tg_Bot.keyboards import (
    start_usage_keyboard, back_to_main_keyboard,
    after_add_keyboard, pagination_keyboard,
    not_found_account_keyboard, change_account_keyboard,
    after_making_keyboard, back_to_home,
    after_refactor_keyboard,
    refactor_phrase, add_delete_phrase
)

from database import db
from config import PAGE_SIZE

router = Router()

class AddPhrase(StatesGroup):
    waiting_for_phrase = State()

class RefactorPhrase(StatesGroup):
    waiting_for_phrase = State()

class AddAccount(StatesGroup):
    waiting_for_name = State()

class RefactorAccount(StatesGroup):
    waiting_for_name = State()

async def send_main_menu(message: types.Message, edit: bool = False):
    welcome_text = (
        "👋 *Вітаю у системі моніторингу!*\n\n"
        "Я твій автоматизований помічник для роботи з Instagram. "
        "Мої головні завдання:\n"
        "📍 *Керувати* списком цілей для парсингу\n"
        "📊 *Стежити* за новими публікаціями\n\n"
        "🚀 *Готовий розпочати?* Обирай розділ нижче:"
    )

    keyboard = await start_usage_keyboard()

    if edit:
        await message.edit_text(welcome_text, parse_mode="Markdown", reply_markup=keyboard)
    else:
        await message.answer(welcome_text, parse_mode="Markdown", reply_markup=keyboard)

@router.message(CommandStart())
async def start(message: types.Message):
    await send_main_menu(message)

@router.callback_query(F.data == "back_to_main")
async def goHome(callback_query: types.CallbackQuery):
    await callback_query.answer()

    await send_main_menu(callback_query.message, edit=True)

@router.callback_query(F.data.startswith("no_action"))
async def no_action_but(callback_query:types.CallbackQuery):
    await callback_query.answer()

@router.callback_query(F.data == "my_phrase")
async def viewPhrase(callback_query: types.CallbackQuery):
    await callback_query.answer()

    text_phrase = await db.get_phrase()

    if not text_phrase:
        text = (
            "<b>📍 Фраза під постом</b>\n\n"
            "⚠️ Наразі фраза <b>не встановлена</b>.\n"
            "Бот буде надсилати пости без додаткового тексту."
        )
        keyboard = await add_delete_phrase()
    else:
        text = (
            "<b>📍 Поточна фраза під постом:</b>\n\n"
            f"<blockquote>{text_phrase}</blockquote>\n\n"
            "<i>Цей текст буде автоматично додаватися до кожного вашого поста.</i>"
        )
        keyboard = await refactor_phrase()
    
    await callback_query.message.edit_text(
        text=text,
        parse_mode="HTML",
        reply_markup=keyboard
    )

@router.callback_query(F.data == "add_phrase")
async def addPhraseStart(callback_query: types.CallbackQuery, state: FSMContext):
    callback_query.answer()

    await callback_query.message.edit_text(
        "📝 <b>Встановлення фрази</b>\n\n"
        "Надішліть фразу, яку бот буде ліпити під кожним постом.\n"
        "Можна з посиланнями та емодзі.",
        parse_mode="HTML"
    )

    await state.set_state(AddPhrase.waiting_for_phrase)

@router.message(AddPhrase.waiting_for_phrase)
async def addPhraseContinue(message: types.Message, state: FSMContext):
    normal_text = message.text.strip()
    
    await db.add_refactor_phrase(normal_text)

    text = (
        "✅ <b>Фразу успішно збережено!</b>\n"
        "__________________________________\n\n"
        "<b>📍 Поточна фраза під постом:</b>\n\n"
        f"<blockquote>{normal_text}</blockquote>\n\n"
        "<i>Цей текст буде автоматично додаватися до кожного вашого поста.</i>"
    )
    
    keyboard = await refactor_phrase()

    await message.answer(
        text=text,
        parse_mode="HTML",
        reply_markup=keyboard
    )

    await state.clear()

@router.callback_query(F.data == "refactor_phrase")
async def refactorPhraseStart(callback_query: types.CallbackQuery, state: FSMContext):
    callback_query.answer()

    await callback_query.message.edit_text(
        "🔄 <b>Зміна фрази під постом</b>\n\n"
        "Надішліть новий текст прямо сюди.\n"
        "Попередній варіант буде автоматично замінено на новий. 👇",
        parse_mode="HTML"
    )

    await state.set_state(RefactorPhrase.waiting_for_phrase)

@router.message(RefactorPhrase.waiting_for_phrase)
async def refactorPhraseContinue(message: types.Message, state: FSMContext):
    normal_text = message.text.strip()
    
    await db.add_refactor_phrase(normal_text)

    text = (
        "✅ <b>Фразу успішно змінена!</b>\n"
        "__________________________________\n\n"
        "<b>📍 Поточна фраза під постом:</b>\n\n"
        f"<blockquote>{normal_text}</blockquote>\n\n"
        "<i>Цей текст буде автоматично додаватися до кожного вашого поста.</i>"
    )
    
    keyboard = await refactor_phrase()

    await message.answer(
        text=text,
        parse_mode="HTML",
        reply_markup=keyboard
    )

    await state.clear()

@router.callback_query(F.data == "delete_phrase")
async def deletePhrase(callback_query: types.CallbackQuery):
    await callback_query.answer()

    await db.delete_phrase()

    text = (
        "🗑️ <b>Фразу під постом видалено</b>\n\n"
        "Тепер пости будуть надсилатися без додаткового тексту.\n"
        "Ви можете встановити нову фразу в будь-який момент."
    )

    keyboard = await add_delete_phrase()

    await callback_query.message.edit_text(
        text=text,
        parse_mode="HTML",
        reply_markup=keyboard
    )

@router.callback_query(F.data == "my_accounts")
async def accountUsage(callback_query: types.CallbackQuery):
    await callback_query.answer()

    all_accounts = await db.get_accounts()

    if not all_accounts:
        text = (
            "📂 *Твій список акаунтів поки що порожній*\n\n"
            "😱 Схоже, ти ще не додав жодного профілю для моніторингу.\n"
            "🚀 Щоб почати збирати дані, просто натисни кнопку додавання нижче!\n\n"
            "✨ *Парсинг стане доступним одразу після налаштування першого профілю.*"
        )

        keyboard = await back_to_main_keyboard()

        await callback_query.message.edit_text(
            text,
            parse_mode="Markdown",
            reply_markup=keyboard
        )
    else:
        text, keyboard = await pagination_keyboard(1, PAGE_SIZE, all_accounts)
        await callback_query.message.edit_text(
            text,
            parse_mode="Markdown",
            reply_markup=keyboard
        )

@router.callback_query(F.data.startswith("page:"))
async def change_page(callback_query: types.CallbackQuery):
    await callback_query.answer()

    page = int(callback_query.data.split(":")[1])

    all_accounts = await db.get_accounts()

    if not all_accounts:
        text = (
            "📂 *Твій список акаунтів поки що порожній*\n\n"
            "😱 Схоже, ти ще не додав жодного профілю для моніторингу.\n"
            "🚀 Щоб почати збирати дані, просто натисни кнопку додавання нижче!\n\n"
            "✨ *Парсинг стане доступним одразу після налаштування першого профілю.*"
        )

        keyboard = await back_to_main_keyboard()

        await callback_query.message.edit_text(
            text,
            parse_mode="Markdown",
            reply_markup=keyboard
        )
    else:
        text, keyboard = await pagination_keyboard(page, PAGE_SIZE, all_accounts)
        await callback_query.message.edit_text(
            text,
            parse_mode="Markdown",
            reply_markup=keyboard
        )

@router.callback_query(F.data.startswith("element:"))
async def start_setting_account(callback_query: types.CallbackQuery):
    await callback_query.answer()

    account_id = int(callback_query.data.split(":")[1])
    
    account = await db.get_one_account(account_id)

    if account:
        text = (
            f"⚙️ **Керування акаунтом**\n\n"
            f"👤 **Назва:** `{account['name']}`\n\n"
            f"🆔 **ID в системі:** `{account['id']}`\n\n"
            f"📅 **Дата додавання:** {account['created_at'].strftime('%d.%m.%Y %H:%M')}\n\n"
            f"Оберіть дію для цього профілю:"
        )
        keyboard = await change_account_keyboard(account_id)
    else:
        text = (
            "⚠️ **Упс! Акаунт не знайдено**\n\n"
            "Схоже, цей профіль було видалено або переміщено. "
            "Дані в списку могли застаріти.\n\n"
            "🔄 *Будь ласка, поверніться назад та оновіть список.*"
        )
        keyboard = await not_found_account_keyboard()

    await callback_query.message.edit_text(
        text,
        parse_mode='Markdown',
        reply_markup=keyboard
    )

@router.callback_query(F.data.startswith("delete:"))
async def delete_account(callback_query: types.CallbackQuery):
    callback_query.answer()

    account_id = int(callback_query.data.split(":")[1])

    await db.delete_account(account_id)

    text = (
        "🗑 **Операція завершена**\n\n"
        f"✨ Акаунт 🆔 `#{account_id}`.\n"
        "♻️ Ваш список акаунтів було оновлено.\n\n"
        "*Ви можете повернутися до переліку або в головне меню.*"
    )

    keyboard = await after_making_keyboard()

    await callback_query.message.edit_text(
        text,
        parse_mode='Markdown',
        reply_markup=keyboard
    )

@router.callback_query(F.data.startswith("refactor:"))
async def start_refactor_account(callback_query: types.CallbackQuery, state: FSMContext):
    callback_query.answer()

    account_id = int(callback_query.data.split(":")[1])
    await state.update_data(refactor_id=account_id)

    await callback_query.message.edit_text(
        "🔄 **Редагування акаунта**\n\n"
        "Введіть **нову назву** для цього Instagram-профілю.\n"
        "Надішліть юзернейм (наприклад: `sony`), щоб оновити дані.\n\n"
        "⚠️ _Стара назва буде замінена на нову!_",
        parse_mode="Markdown"
    )

    await state.set_state(RefactorAccount.waiting_for_name)

@router.message(RefactorAccount.waiting_for_name)
async def process_refactor(message: types.Message, state: FSMContext):
    name = message.text.strip()

    data = await state.get_data()
    account_id = data.get('refactor_id')

    if not account_id:
        keyboard = await back_to_home()
        await message.answer(
            "❌ Сталася помилка: ID акаунта втрачено. Почніть спочатку.",
            parse_mode="Markdown",
            reply_markup=keyboard
        )
        await state.clear()
        return

    result = await db.update_account_name(account_id, name)

    if result == "success":
        await state.clear()
        text = (
            "✅ **Назву успішно змінено!**\n\n"
            f"Тепер цей акаунт підписаний як: `{name}`\n"
            "Дані в базі оновлено миттєво. ✨"
        )
        keyboard = await after_refactor_keyboard(account_id)
    elif result == "not_found":
        await state.clear()
        text = (
            "❌ **Помилка оновлення**\n\n"
            "Не вдалося знайти цей акаунт у системі. Можливо, він був видалений раніше іншим адміністратором."
        )
        keyboard = await after_making_keyboard()
    elif result == 'already_exists':
        text = (
            "⚠️ **Ця назва вже зайнята!**\n\n"
            f"Акаунт з іменем `{name}` вже є у вашому списку.\n"
            "Будь ласка, введіть **іншу** назву для рефакторингу:"
        )
        keyboard = None
    else:
        await state.clear()
        text = (
            "🆘 **Технічний збій**\n\n"
            "Сталася невідома помилка при спробі оновити базу даних. Спробуйте пізніше або зверніться до розробника."
        )
        keyboard = await after_refactor_keyboard(account_id)
    
    await message.answer(
        text,
        parse_mode="Markdown",
        reply_markup=keyboard
    )

@router.callback_query(F.data == "add_account")
async def start_add_account(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()

    await callback_query.message.edit_text(
        "📝 *Введіть назву Instagram-акаунта*\n\n"
        "Надішліть мені юзернейм (наприклад: `apple`).\n"
        "Переконайтеся, що акаунт відкритий! 🔓",
        parse_mode="Markdown"
    )

    await state.set_state(AddAccount.waiting_for_name)

@router.message(AddAccount.waiting_for_name)
async def process_add(message: types.Message, state: FSMContext):
    name = message.text.strip()
    result = await db.add_account(name)

    if result == True:
        await state.clear()
        
        keyboard = await after_add_keyboard()

        await message.answer(
            f"✅ Акаунт `{name}` додано!",
            parse_mode="Markdown",
            reply_markup=keyboard
        )
    elif result == False:
        await state.clear()

        keyboard = await after_add_keyboard()

        await message.answer(
            f"ℹ️ Акаунт `{name}` вже відстежується.",
            parse_mode="Markdown",
            reply_markup=keyboard
        )
    else:
        await message.answer(
            "❌ Сталася технічна помилка при доступі до бази даних.\n"
            "Спробуйте, ще раз."
            "Надішліть мені юзернейм (наприклад: `apple`).\n"
        )
