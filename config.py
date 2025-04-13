import json
import os
import re
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

def extract_emails(text: str) -> list[str]:
    # Простое и надёжное регулярное выражение
    email_regex = r'[\w\.-]+@[\w\.-]+\.\w+'
    return re.findall(email_regex, text)


class Settings(BaseSettings):
    sender_email: str
    smtp_server: str
    smtp_port: int
    login: str
    password: str
    signature: str = ""
    text: str
    subject: str
    recipients: list

    model_config = SettingsConfigDict(extra="ignore")

    @classmethod
    def from_json(
        cls,
        path: str = "./params.json",
        recipients_file: str = "./recipients.txt"
    ):

        with open(path, encoding="utf-8") as f:
            data = json.load(f)

        if os.path.exists(recipients_file):
            with open(recipients_file, encoding="utf-8") as f:
                recipients = extract_emails(f.read())
            data["recipients"] = recipients
        return cls(**data)


settings = Settings.from_json()
