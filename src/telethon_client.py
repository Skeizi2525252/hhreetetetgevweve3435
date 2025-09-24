from __future__ import annotations

import os
from telethon import TelegramClient
from telethon.sessions import StringSession


class TelethonAuthService:
    def __init__(self, api_id: int, api_hash: str, session_dir: str) -> None:
        self.api_id = api_id
        self.api_hash = api_hash
        self.session_dir = session_dir
        os.makedirs(session_dir, exist_ok=True)

    def _session_path(self, name: str) -> str:
        safe = "".join(c for c in name if c.isalnum() or c in ("_", "-"))
        return os.path.join(self.session_dir, f"{safe}.session")

    def create_client(self, session_name: str = "owner") -> TelegramClient:
        session_file = self._session_path(session_name)
        client = TelegramClient(session_file, self.api_id, self.api_hash)
        return client
