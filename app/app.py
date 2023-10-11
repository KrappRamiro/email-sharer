from fastapi import FastAPI, Request, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from tempfile import SpooledTemporaryFile


from utils.EmailParser import EmailParser
from utils.user import User
from utils.email import Email
from utils.tempfile_utils import get_temp_file_from_disk, save_uploaded_file_to_disk

#! TODO: Que se agreguen todos los emails en mails/ al current_user cuando se loadee

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/static/css", StaticFiles(directory="static/css"), name="css")
app.mount("/static/img", StaticFiles(directory="static/img"), name="img")
app.mount("/static/js", StaticFiles(directory="static/js"), name="js")
app.mount("/mails", StaticFiles(directory="mails"), name="mails")
templates = Jinja2Templates(directory="templates")


def remove_parentheses(value):
    if value.startswith("('") and value.endswith("',)"):
        return value[2:-3]
    return value


def get_email_file_as_dict(name: str) -> dict:
    path = f"mails/{name}"

    spooled_temp_file = get_temp_file_from_disk(path)
    parser = EmailParser()
    return parser.parse(spooled_temp_file, filename=name)


def add_email_to_user(user: User, email_file: SpooledTemporaryFile, filename: str):
    parser = EmailParser()
    parsed_email = parser.parse(email_file, filename)
    user.add_email(Email(**parsed_email))


def initialize_emails_to_user(user: User) -> None:
    for email_filename in os.listdir("mails/"):
        print(email_filename)
        temp_file = get_temp_file_from_disk(f"mails/{email_filename}")
        add_email_to_user(user, email_file=temp_file, filename=email_filename)


current_user = User(
    name="Sandra Rodriguez",
    id="01a",
)

initialize_emails_to_user(current_user)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "current_user": current_user,
        },
    )


# region
# -------------------------------------------- #


@app.post("/email/parse")
async def parse_email(email: UploadFile):
    try:
        parser = EmailParser()
        return parser.parse(email.file, email.filename)
    except ValueError:
        raise HTTPException(status_code=422, detail="File not supported")


@app.post("/email/upload")
async def upload_email(email: UploadFile):
    if email.filename == "":
        raise HTTPException(status_code=400, detail=f"File should have a name or exist")
    email.filename = email.filename.replace(" ", "-")
    save_uploaded_file_to_disk(email.file, email.filename)
    add_email_to_user(current_user, email.file, email.filename)


@app.get("/email/get/file")
async def get_email_as_file(name: str):
    path = f"mails/{name}"
    if not os.path.exists(path):
        return HTTPException(status_code=404, detail=f"File {path} not found")
    return FileResponse(path)


@app.get("/email/get/json")
async def get_email_as_json(name: str):
    return get_email_file_as_dict(name)


@app.get("/email/get/html")
async def get_email_as_html(name: str):
    """
    Si tenes ����� en el email, https://answers.microsoft.com/en-us/windows/forum/all/why-do-i-see-black-diamonds-with-question-marks-in/e82c68ce-9e3e-4234-8d7d-0c85d2d1a1d9
    """
    path = f"mails/{name}"
    return FileResponse(path, media_type="text/html")


@app.get("/email/list")
async def get_list_email():
    file_list = os.listdir("mails/")
    return file_list


# endregion
# -------------------------------------------- #


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
