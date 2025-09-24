## Self-Auth Telegram Bot (aiogram + Telethon)

This bot lets only the owner authorize their own Telegram account via Telethon using an inline keypad for entering the login code.

### Setup

1) Create venv and install deps:
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

2) Create `.env` from example:
```bash
cp .env.example .env
```
Set:
- BOT_TOKEN
- API_ID / API_HASH
- SESSION_DIR (default ./sessions)
- OWNER_TELEGRAM_ID (your numeric Telegram ID)

### Run
```bash
python -m src
```

### Flow
- Start: `/start` shows button "Авторизоваться" (shares contact)
- Bot sends login code request via Telethon to your number
- Inline keypad `1..9,0,⌫,✅` to input code
- On success, Telethon session saved in `SESSION_DIR`
