# SQLAlchemy uses the term "model" to refer to these classes and instances that interact with the database.
# But Pydantic also uses the term "model" to refer to something different, the data validation, conversion, and documentation classes and instances.

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    emails = relationship(
        "Email", back_populates="owner"
    )  # back_populates value must be the name of the variable in the other class


class Email(Base):
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    subject = Column(String(400), nullable=False)
    sender = Column(String, nullable=False)
    recipients = Column(String, nullable=False)
    cc = Column(String, default=None)
    bcc = Column(String, default=None)
    date = Column(String, nullable=False)
    body = Column(String, nullable=False)
    filename = Column(String, nullable=False)

    # Relationship with User.emails
    owner = relationship("User", back_populates="emails")
    # Relationship with Attachment.email
    attachments = relationship("Attachment", back_populates="email")


class Attachment(Base):
    __tablename__ = "attachments"

    id = Column(Integer, primary_key=True, index=True)
    email_id = Column(Integer, ForeignKey("emails.id"), nullable=False)
    filename = Column(String, nullable=False)
    # Relationship with Email.attachments
    email = relationship("Email", back_populates="attachments")
