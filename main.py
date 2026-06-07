from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,
)

from database import init_db
from config import BOT_TOKEN
from handlers import (
    start,
    help_command,
    about,
    user_id,
    handle_text,
    ping,
    handle_text,
    menu,
    button_callback,
    state,
    whereami,
    data,
    profile_command,
    db_profile,
    db_users,
    set_theme,
    db_settings,
    db_messages,
    db_messages_count,
    clear_messages,
)


def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN отсутствует")
    
    init_db()

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(CommandHandler("id", user_id))
    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CommandHandler("state", state))
    app.add_handler(CommandHandler("whereami", whereami))
    app.add_handler(CommandHandler("data", data))
    app.add_handler(CommandHandler("profile", menu))    
    app.add_handler(CommandHandler("db_profile", db_profile))
    app.add_handler(CommandHandler("db_users", db_users))
    app.add_handler(CommandHandler("set_theme", set_theme))
    app.add_handler(CommandHandler("db_settings", db_settings))
    app.add_handler(CommandHandler("db_messages", db_messages))
    app.add_handler(CommandHandler("db_messages_count", db_messages_count))
    app.add_handler(CommandHandler("clear_messages", clear_messages))
    app.add_handler(CallbackQueryHandler(button_callback))


    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_text,
        )
    )

    print("Bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()