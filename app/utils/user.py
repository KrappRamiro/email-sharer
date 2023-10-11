from .email import Email
from typing import List


class User:
    def __init__(self, name: str, id: str, owned_emails: List[Email] | None = None) -> None:
        self.name = name
        self.id = id
        self.owned_emails = owned_emails if owned_emails is not None else []

    def add_email(self, email: Email) -> list:
        self.owned_emails.append(email)
