from keyboards import get_main_menu_keyboard, get_back_keyboard, get_settings_keyboard
async def render_main_menu(query):
    await query.edit_message_text(
        "Главное меню:",
        reply_markup=get_main_menu_keyboard(),
    )


async def render_simple_screen(query, text):
    await query.edit_message_text(
        text,
        reply_markup=get_back_keyboard(),
    )


async def render_about_screen(query):
    await render_simple_screen(query, "Это раздел About.")


async def render_ping_screen(query):
    await render_simple_screen(query, "pong")


async def render_profile_screen(query, context):
    name = context.user_data.get("name", "не указано")
    age = context.user_data.get("age", "не указано")
    city = context.user_data.get("city", "не указано")

    text = f"Профиль\n\nИмя: {name}\nВозраст: {age}\nГород: {city}"

    await render_simple_screen(query, text)


async def render_settings_screen(query, context):
    theme = context.user_data.get("theme", "dark")
    notifications = context.user_data.get(
        "notifications",
        "enabled"
    )

    text = (
        "Settings\n\n"
        f"Theme: {theme}\n"
        f"Notifications: {notifications}"
    )

    await query.edit_message_text(
        text,
        reply_markup=get_settings_keyboard(),
    )


async def render_set_name_screen(query):
    await query.edit_message_text(
        "Введите ваше имя обычным сообщением:"
    )


async def render_set_age_screen(query):
    await query.edit_message_text(
        "Введите ваш возраст:"
    )


async def render_set_city_screen(query):
    await query.edit_message_text(
        "Введите ваш город:"
    )