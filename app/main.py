from fastapi import FastAPI, Request, UploadFile, HTTPException, Depends
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from tempfile import SpooledTemporaryFile
from sqlalchemy.orm import Session
from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine

from utils.EmailParser import EmailParser


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency, see https://fastapi.tiangolo.com/tutorial/sql-databases/#create-a-dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/static/css", StaticFiles(directory="static/css"), name="css")
app.mount("/static/img", StaticFiles(directory="static/img"), name="img")
app.mount("/static/js", StaticFiles(directory="static/js"), name="js")
app.mount("/mails", StaticFiles(directory="mails"), name="mails")
templates = Jinja2Templates(directory="templates")


@app.post("/email/parse")
async def parse_email(email: UploadFile):
    """
    Parse an email attachment and return its contents.

    Args:
        email (UploadFile): The email attachment to parse.

    Returns:
        dict: Parsed email contents.

    Raises:
        HTTPException: If the file is not supported.
    """
    try:
        parser = EmailParser()
        return parser.parse(email.file, email.filename)
    except ValueError:
        raise HTTPException(status_code=422, detail="File not supported")


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user.

    Args:
        user (schemas.UserCreate): User information.

    Returns:
        schemas.User: The created user.

    Raises:
        HTTPException: If the email is already registered.
    """
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get a list of users.

    Args:
        skip (int): Number of users to skip.
        limit (int): Maximum number of users to return.

    Returns:
        list[schemas.User]: List of users.
    """
    users = crud.get_users(db, skip, limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """
    Get user information by user ID.

    Args:
        user_id (int): User ID.

    Returns:
        schemas.User: User information.

    Raises:
        HTTPException: If the user is not found.
    """
    db_user = crud.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    return db_user


@app.post("/users/{user_id}/email/", response_model=schemas.Email)
def create_email_for_user(
    user_id: int,
    email: schemas.EmailCreate,
    db: Session = Depends(get_db),
):
    """
    Create an email for a specific user.

    Args:
        user_id (int): User ID.
        email (schemas.EmailCreate): Email information.

    Returns:
        schemas.Email: The created email.
    """
    return crud.create_email(db=db, email=email, user_id=user_id)


@app.get("/users/{user_id}/emails/", response_model=list[schemas.Email])
def get_user_emails(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get a list of emails for a specific user.

    Args:
        user_id (int): User ID for whom emails are retrieved.
        skip (int): Number of emails to skip.
        limit (int): Maximum number of emails to return.

    Returns:
        list[schemas.Email]: List of emails for the user.
    """
    return crud.get_emails_by_user(
        db=db,
        user_id=user_id,
        skip=skip,
        limit=limit,
    )


@app.get("/emails/", response_model=list[schemas.Email])
def read_emails(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get a list of emails.

    Args:
        skip (int): Number of emails to skip.
        limit (int): Maximum number of emails to return.

    Returns:
        list[schemas.Email]: List of emails.
    """
    emails = crud.get_emails(db, skip=skip, limit=limit)
    return emails


@app.post("/emails/{email_id}/attachments", response_model=schemas.Attachment)
def add_attachment_to_email(
    email_id: int, attachment: schemas.Attachment, db: Session = Depends(get_db)
):
    """
    Add an attachment to a specific email.

    Args:
        email_id (int): ID of the email to which the attachment will be added.
        attachment (schemas.Attachment): Attachment information to be added.

    Returns:
        schemas.Attachment: The added attachment.
    """
    return crud.add_attachment_to_email(db=db, attachment=attachment, email_id=email_id)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
