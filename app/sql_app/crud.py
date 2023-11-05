from sqlalchemy.orm import Session
from typing import List

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password, name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_email(db: Session, email_id: int):
    return db.query(models.Email).filter_by(email_id=email_id).first()


def get_emails(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Email).offset(skip).limit(limit).all()


def get_emails_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Email).filter(models.User.id == user_id).offset(skip).limit(limit).all()
    )


def create_email(db: Session, email_data: schemas.Email, file: bytes, user_id: int):
    db_item = models.Email(**email_data.model_dump(), owner_id=user_id, file=file)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def add_attachment_to_email(db: Session, attachment: bytes, email_id: int):
    db_item = models.Attachment(**attachment.model_dump(), email_id=email_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_email_attachments(db: Session, email_id: int, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Attachment)
        .filter(models.Email.id == email_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
