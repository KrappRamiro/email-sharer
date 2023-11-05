from pydantic import BaseModel


class Attachment(BaseModel):
    id: int
    email_id: int
    filename: str

    class Config:
        orm_mode = True


class EmailBase(BaseModel):
    # All the domain stuff
    subject: str
    sender: str
    recipients: str
    cc: str | None
    bcc: str | None
    date: str
    body: str


class EmailCreate(EmailBase):
    pass


class Email(EmailBase):
    id: int
    owner_id: int
    filename: str
    attachments: list[Attachment] = []

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    # All the domain stuff here
    name: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    emails: list[Email] = []

    class Config:
        orm_mode = True
