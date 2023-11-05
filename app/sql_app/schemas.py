from pydantic import BaseModel

"""
Difference between ItemBase and Item

ItemBase (Input Model): 
ItemBase is an input model used for creating or updating items. It defines the fields that are expected when creating or updating an item. It's a subclass of BaseModel and includes the title and description fields. You can use this model to validate the data sent in requests to create or update items.

Item (Output Model):
Item is an output model used for representing items when they are retrieved from the database or returned in API responses. It includes additional fields like id and owner_id, which are part of the database model.
It also specifies the from_attributes(previously orm_mode) = True configuration, which tells FastAPI to convert the model to and from an ORM model (the SQLAlchemy model) automatically. This means that when you return an Item in a response, FastAPI will use the ORM model to fetch the corresponding data from the database and populate the response object.

By having separate input and output models, you can control what data is accepted in requests and what data is returned in responses, and you can keep the input model (e.g., ItemCreate) and output model (e.g., Item) separate to avoid confusion or bugs. It also allows you to add or remove fields from the output model without affecting the input model or vice versa. This separation of concerns and flexibility is a good practice in FastAPI development.

"""


# ? Reminder, dont add file in the schemas, just ask for it as a parameter in the crud functions


class AttachmentBase(BaseModel):
    filename: str


class AttachmentCreate(AttachmentBase):
    pass


class Attachment(AttachmentBase):
    id: int
    email_id: int

    class Config:
        from_attributes = True


class EmailBase(BaseModel):
    # All the domain stuff
    subject: str
    sender: str
    recipients: str
    cc: str | None
    bcc: str | None
    date: str
    body: str
    filename: str
    attachments: list[Attachment] = []


class EmailCreate(EmailBase):
    pass


class Email(EmailBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True


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
        from_attributes = True
