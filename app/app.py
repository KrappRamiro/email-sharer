from fastapi import FastAPI, Request, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import extract_msg
import eml_parser
import os
from tempfile import SpooledTemporaryFile
from datetime import datetime


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/static/css", StaticFiles(directory="static/css"), name="css")
app.mount("/static/img", StaticFiles(directory="static/img"), name="img")
app.mount("/static/js", StaticFiles(directory="static/js"), name="js")
app.mount("/mails", StaticFiles(directory="mails"), name="mails")
templates = Jinja2Templates(directory="templates")


class EmailParser:
    def parse(self, email: SpooledTemporaryFile, filename: str) -> dict:
        file_extension = os.path.splitext(filename)[-1].lower().removeprefix(".")  # eml or msg
        if file_extension == "eml":
            return self._parse_eml(email)
        elif file_extension == "msg":
            return self._parse_msg(email)
        else:
            raise ValueError(f"Invalid email type {file_extension}. Use msg or eml")

    def _parse_msg(self, file: SpooledTemporaryFile) -> dict:
        email = {}

        msg = extract_msg.Message(file)
        email["subject"] = msg.subject
        email["sender"] = msg.sender
        email["recipients"] = msg.to
        email["cc"] = msg.cc
        email["bcc"] = msg.bcc
        email["date"] = msg.date
        email["body"] = msg.body
        attachments = []
        for attachment in msg.attachments:
            attachments.append(attachment.getFilename())
        email["attachments"] = attachments
        return email

    def _parse_eml(self, email: SpooledTemporaryFile) -> dict:
        parser = eml_parser.EmlParser(include_raw_body=True, include_attachment_data=True)
        eml_bytes = email.read()
        parsed_eml = parser.decode_email_bytes(eml_bytes)
        return parsed_eml


def get_temp_file(path: str) -> SpooledTemporaryFile:
    if not os.path.exists(path):
        return HTTPException(status_code=404, detail=f"File {path} not found")

    # Create a SpooledTemporaryFile
    spooled_temp_file = SpooledTemporaryFile(max_size=2000)
    # Open the file you want to read from filesystem
    with open(path, "rb") as f:
        # Read the content of the file
        data = f.read()
        # Write the content to the SpooledTemporaryFile
        spooled_temp_file.write(data)

    spooled_temp_file.seek(0)
    return spooled_temp_file


def save_uploaded_file(in_file: SpooledTemporaryFile, filename):
    # https://stackoverflow.com/a/63581187/15965186
    current_time = datetime.now()
    current_time = current_time.strftime("%Y-%m-%d-%H-%M-%S")
    out_file_path = f"mails/{current_time}_{filename}"
    print(f"Saving file to {out_file_path}")

    with open(out_file_path, "wb") as out_file:
        while content := in_file.read(1024):  # read chunk
            out_file.write(content)  # write chunk


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "current_user": "01a"})


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
    email.filename = email.filename.replace(" ", "-")
    save_uploaded_file(email.file, email.filename)


@app.get("/email/get/file")
async def get_email_as_file(name: str):
    path = f"mails/{name}"
    if not os.path.exists(path):
        return HTTPException(status_code=404, detail=f"File {path} not found")
    return FileResponse(path)


@app.get("/email/get/json")
async def get_email_as_json(name: str):
    path = f"mails/{name}"

    spooled_temp_file = get_temp_file(path)
    parser = EmailParser()
    return parser.parse(spooled_temp_file, filename=name)


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


# -------------------------------------------- #


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
