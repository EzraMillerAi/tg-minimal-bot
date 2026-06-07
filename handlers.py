import os

from dotenv import load_dotenv

from ai_service import generate_ai_response
from database import clear_user_messages, get_recent_messages_for_ai, get_messages_count, save_user_profile, load_user_profile, get_user_profile, get_all_users,save_user_settings, get_user_settings, save_message, get_user_messages    
from telegram import Update
from telegram.ext import ContextTypes
from keyboards import get_main_menu_keyboard, get_back_keyboard , get_success_keyboard
from states import NAVIGATION_MAP, INPUT_STATES, SCREEN_RENDERERS
from renderers import (
    render_main_menu,
    render_about_screen,
    render_ping_screen,
    render_profile_screen,
    render_settings_screen,
    render_set_name_screen,
    render_set_age_screen,
    render_set_city_screen,
)

load_dotenv()

AI_HISTORY_LIMIT = int(os.getenv("AI_HISTORY_LIMIT", "10"))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["current_screen"] = "main_menu"
    telegram_id = update.effective_user.id
    profile = load_user_profile(telegram_id)

    if profile:
        context.user_data.update(profile)    

    await update.message.reply_text(
        "Привет. Выбери действие:",
        reply_markup=get_main_menu_keyboard(),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start - запуск бота\n"
        "/help - список команд\n"
        "/about - информация\n"
        "/id - твой Telegram ID\n"
        "/ping - проверка работы бота\n"
        "/menu - интерактивное меню\n"
        "/state - показать текущий экран\n"
        "/whereami - подсказка, где ты находишься\n"
        "В интерактивном меню доступны:\n"
        "- Profile\n"
        "- Settings\n"
        "- Set Name\n"
        "- Set Age\n"
        "- Set City\n"
        "/profile - показать профиль пользователя\n"
    )


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Это minimal stable Telegram bot.\n"
        "Сделан для изучения backend foundations."
    )


async def user_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id

    await update.message.reply_text(
        f"Твой Telegram ID: {telegram_id}"
    )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    current_screen = context.user_data.get("current_screen")
    user_text = update.message.text
    telegram_id = update.effective_user.id

    state_config = INPUT_STATES.get(current_screen)

    if not state_config:
        thinking_message = await update.message.reply_text(
            "Думаю..."
        )

        history = get_recent_messages_for_ai(
            telegram_id=telegram_id,
            limit=AI_HISTORY_LIMIT,
        )

        ai_response = generate_ai_response(
            user_text=user_text,
            history=history,
        )

        save_message(
            telegram_id=telegram_id,
            message_text=user_text,
            role="user",
        )

        save_message(
            telegram_id=telegram_id,
            message_text=ai_response,
            role="assistant",
        )

        await thinking_message.edit_text(ai_response)
        return

    validator = state_config.get("validator")

    if validator == "number":
        if not user_text.isdigit():
            await update.message.reply_text(
                "Значение должно быть числом."
            )
            return

    field_name = state_config["field"]

    context.user_data[field_name] = user_text

    save_message(
        telegram_id=telegram_id,
        message_text=user_text,
        role="user",
    )

    save_user_profile(
        telegram_id=telegram_id,
        name=context.user_data.get("name"),
        age=context.user_data.get("age"),
        city=context.user_data.get("city"),
    )

    context.user_data["current_screen"] = "success"

    success_message = state_config["success_message"]

    await send_success_message(
        update,
        f"{success_message}: {user_text}"
    )

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "pong"
    )

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["current_screen"] = "main_menu"

    await update.message.reply_text(
        "Главное меню:",
        reply_markup=get_main_menu_keyboard(),
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    next_screen = NAVIGATION_MAP.get(query.data)
    renderer = SCREEN_RENDERERS.get(next_screen)

    await query.answer()

    if query.data == "toggle_notifications":
        current_notifications = context.user_data.get("notifications", "enabled")

        if current_notifications == "enabled":
            new_notifications = "disabled"
        else:
            new_notifications = "enabled"

        context.user_data["notifications"] = new_notifications

        save_user_settings(
            telegram_id=update.effective_user.id,
            theme=context.user_data.get("theme", "dark"),
            notifications=new_notifications,
        )
        
    if query.data == "toggle_theme":
        current_theme = context.user_data.get("theme", "dark")

        if current_theme == "dark":
            new_theme = "light"
        else:
            new_theme = "dark"

        context.user_data["theme"] = new_theme

        save_user_settings(
            telegram_id=update.effective_user.id,
            theme=new_theme,
            notifications=context.user_data.get(
                "notifications",
                "enabled"
            ),
        )    

    current_screen = context.user_data.get("current_screen")

    if current_screen == next_screen and query.data not in [
    "toggle_notifications",
    "toggle_theme",
    ]:
        return

    if next_screen:
        context.user_data["current_screen"] = next_screen

    if renderer:
        if next_screen in ["profile", "settings"]:
            await renderer(query, context)
        else:
            await renderer(query)
            
async def state(update: Update, context: ContextTypes.DEFAULT_TYPE):
    current_screen = context.user_data.get("current_screen", "unknown")

    await update.message.reply_text(
        f"Current screen: {current_screen}"
    )
async def whereami(update: Update, context: ContextTypes.DEFAULT_TYPE):
    current_screen = context.user_data.get("current_screen", "unknown")

    if current_screen == "main_menu":
        await update.message.reply_text(
            "Ты сейчас в главном меню. Можно выбрать About или Ping."
        )

    elif current_screen == "about":
        await update.message.reply_text(
            "Ты сейчас в разделе About. Можно нажать Back."
        )

    elif current_screen == "ping":
        await update.message.reply_text(
            "Ты сейчас в разделе Ping. Можно нажать Back."
        )

    else:
        await update.message.reply_text(
            "Я пока не знаю, где ты находишься. Напиши /menu."
        )

async def data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Current screen: {context.user_data.get('current_screen')}\n"
        f"User data:\n{context.user_data}"
    )

async def profile_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Профиль пользователя:\n"
        f"Имя: {context.user_data.get('name', 'не указано')}\n"
        f"Возраст: {context.user_data.get('age', 'не указан')}\n"
        f"Город: {context.user_data.get('city', 'не указан')}\n",
        reply_markup=get_back_keyboard(),
    )    


async def send_success_message(update: Update, text):
    await update.message.reply_text(
        text,
        reply_markup=get_success_keyboard(),
    )

async def db_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    row = get_user_profile(telegram_id)

    if row is None:
        await update.message.reply_text(
            "Профиль в базе данных не найден."
        )
        return

    await update.message.reply_text(
        f"DB Profile\n\n"
        f"Telegram ID: {row[0]}\n"
        f"Name: {row[1]}\n"
        f"Age: {row[2]}\n"
        f"City: {row[3]}"
    )        

async def db_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    rows = get_all_users()

    if not rows:
        await update.message.reply_text(
            "В базе данных пока нет пользователей."
        )
        return

    text = f"Users in DB: {len(rows)}\n\n"

    for row in rows:
        telegram_id, name, age, city = row

        text += (
            f"ID: {telegram_id}\n"
            f"Name: {name}\n"
            f"Age: {age}\n"
            f"City: {city}\n\n"
        )

    await update.message.reply_text(text)


async def set_theme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id

    save_user_settings(
        telegram_id=telegram_id,
        theme="dark",
        notifications="enabled",
    )

    await update.message.reply_text(
        "Настройки сохранены: theme=dark, notifications=enabled"
    )

async def db_settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    row = get_user_settings(telegram_id)

    if row is None:
        await update.message.reply_text(
            "Настройки в базе данных не найдены."
        )
        return

    theme, notifications = row

    await update.message.reply_text(
        f"DB Settings\n\n"
        f"Theme: {theme}\n"
        f"Notifications: {notifications}"
    )

async def db_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id

    rows = get_user_messages(telegram_id)

    if not rows:
        await update.message.reply_text(
            "Сообщений не найдено."
        )
        return

    text = "Last messages:\n\n"

    for row in rows:
        role, message_text = row
        text += f"- {role}: {message_text}\n"

    await update.message.reply_text(text)

async def db_messages_count(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    telegram_id = update.effective_user.id

    count = get_messages_count(telegram_id)

    await update.message.reply_text(
        f"Messages count: {count}"
    )

async def clear_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id

    clear_user_messages(telegram_id)

    await update.message.reply_text(
        "История сообщений очищена."
    )    
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
