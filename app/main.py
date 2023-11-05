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
    try:
        parser = EmailParser()
        return parser.parse(email.file, email.filename)
    except ValueError:
        raise HTTPException(status_code=422, detail="File not supported")


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip, limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    return db_user


@app.post("/users/{user_id}/email/")
def create_email_for_user(
    user_id: int,
    email: schemas.EmailCreate,
    db: Session = Depends(get_db),
):
    return crud.create_email(db=db, email=email, user_id=user_id)


@app.get("/emails/", response_model=list[schemas.Email])
def read_emails(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    emails = crud.get_emails(db, skip=skip, limit=limit)
    return emails


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
