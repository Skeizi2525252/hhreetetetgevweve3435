from telegram import Update
from telegram.ext import ContextTypes

from src.keyboards import build_code_inline_kb, build_login_reply_keyboard
from src.state import AuthState
from src.telethon_client import TelethonAuthService
from src.config import load_settings


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state = context.user_data.setdefault("auth", AuthState(step="idle"))
    state.step = "waiting_contact"
    await update.effective_message.reply_text(
        "Привет! Нажмите кнопку ниже, чтобы авторизоваться.",
        reply_markup=build_login_reply_keyboard(),
    )


async def on_contact(update: Update, context: ContextTypes.DEFAULT_TYPE, auth: TelethonAuthService):
    settings = load_settings()
    if update.effective_user.id != settings.owner_telegram_id:
        await update.effective_message.reply_text("Доступ запрещён.")
        return

    contact = update.effective_message.contact
    if not contact or not contact.phone_number:
        await update.effective_message.reply_text("Пожалуйста, отправьте контакт через кнопку.")
        return

    state: AuthState = context.user_data.setdefault("auth", AuthState(step="idle"))
    state.step = "waiting_code"
    state.phone_number = contact.phone_number
    state.code = ""

    client = auth.create_client("owner")
    await client.connect()
    try:
        if await client.is_user_authorized():
            await update.effective_message.reply_text("Сессия уже активна. Готово.")
            state.step = "idle"
            return
        await client.send_code_request(state.phone_number)
        await update.effective_message.reply_text("Отправьте код через клавиатуру:", reply_markup=build_code_inline_kb(""))
    finally:
        await client.disconnect()


async def on_code(update: Update, context: ContextTypes.DEFAULT_TYPE, auth: TelethonAuthService):
    if not update.callback_query or not update.callback_query.data:
        return
    await update.callback_query.answer()
    _, _, key = update.callback_query.data.partition(":")

    state: AuthState = context.user_data.setdefault("auth", AuthState(step="idle"))
    current = state.code

    if key == "noop":
        return

    if key == "⌫":
        state.code = current[:-1]
        await update.callback_query.message.edit_reply_markup(build_code_inline_kb(state.code))
        return

    if key == "✅":
        client = auth.create_client("owner")
        await client.connect()
        try:
            if await client.is_user_authorized():
                await update.effective_message.reply_text("Сессия уже активна. Готово.")
                state.step = "idle"
                return
            try:
                await client.sign_in(phone=state.phone_number, code=state.code)
                await update.effective_message.reply_text("Успешная авторизация. Сессия сохранена.")
                state.step = "idle"
            except Exception as e:
                await update.effective_message.reply_text(f"Неверный код или ошибка: {e}")
        finally:
            await client.disconnect()
        return

    if key.isdigit():
        if len(current) >= 8:
            return
        state.code = current + key
        await update.callback_query.message.edit_reply_markup(build_code_inline_kb(state.code))
