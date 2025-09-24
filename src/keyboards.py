from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def build_login_reply_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup([[KeyboardButton("Авторизоваться", request_contact=True)]], resize_keyboard=True, one_time_keyboard=True)
    return kb


def build_code_inline_kb(current: str = "") -> InlineKeyboardMarkup:
    layout = [
        ["1", "2", "3"],
        ["4", "5", "6"],
        ["7", "8", "9"],
        ["0", "⌫", "✅"],
    ]
    buttons = [
        [InlineKeyboardButton(text=label, callback_data=f"code:{label}") for label in row]
        for row in layout
    ]
    if current:
        display = "•" * len(current)
    else:
        display = "—"
    buttons.append([InlineKeyboardButton(text=f"Код: {display}", callback_data="code:noop")])
    return InlineKeyboardMarkup(buttons)
