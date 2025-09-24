from dataclasses import dataclass


@dataclass
class AuthState:
    step: str  # 'idle' | 'waiting_contact' | 'waiting_code'
    phone_number: str = ""
    code: str = ""
