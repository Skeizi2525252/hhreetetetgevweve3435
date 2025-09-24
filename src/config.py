import os
from dataclasses import dataclass
from dotenv import load_dotenv


@dataclass
class Settings:
    bot_token: str
    api_id: int
    api_hash: str
    session_dir: str
    owner_telegram_id: int


def load_settings() -> Settings:
    load_dotenv()
    bot_token = os.getenv("BOT_TOKEN", "").strip()
    api_id_raw = os.getenv("API_ID", "0").strip()
    api_hash = os.getenv("API_HASH", "").strip()
    session_dir = os.getenv("SESSION_DIR", "./sessions").strip()
    owner_id_raw = os.getenv("OWNER_TELEGRAM_ID", "0").strip()

    if not os.path.isdir(session_dir):
        os.makedirs(session_dir, exist_ok=True)

    try:
        api_id = int(api_id_raw)
    except ValueError:
        api_id = 0

    try:
        owner_id = int(owner_id_raw)
    except ValueError:
        owner_id = 0

    return Settings(
        bot_token=bot_token,
        api_id=api_id,
        api_hash=api_hash,
        session_dir=session_dir,
        owner_telegram_id=owner_id,
    )
