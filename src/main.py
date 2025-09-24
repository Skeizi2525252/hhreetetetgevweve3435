import logging

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

from src.config import load_settings
from src.telethon_client import TelethonAuthService
from src.handlers import start as start_handler
from src.handlers import on_contact as contact_handler
from src.handlers import on_code as code_callback_handler


logging.basicConfig(level=logging.INFO)


def create_app():
    settings = load_settings()
    auth_service = TelethonAuthService(settings.api_id, settings.api_hash, settings.session_dir)
    application = ApplicationBuilder().token(settings.bot_token).build()

    application.add_handler(CommandHandler("start", start_handler))
    application.add_handler(MessageHandler(filters.CONTACT, lambda u, c: contact_handler(u, c, auth_service)))
    application.add_handler(CallbackQueryHandler(lambda u, c: code_callback_handler(u, c, auth_service), pattern=r"^code:"))

    return application


def main():
    app = create_app()
    app.run_polling()


if __name__ == "__main__":
    main()
