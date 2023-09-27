from fastapi import FastAPI, Request, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import extract_msg
import eml_parser
import aiofiles
import os
from datetime import datetime


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/static/css", StaticFiles(directory="static/css"), name="css")
app.mount("/static/img", StaticFiles(directory="static/img"), name="img")
app.mount("/static/js", StaticFiles(directory="static/js"), name="js")
app.mount("/mails", StaticFiles(directory="mails"), name="mails")
templates = Jinja2Templates(directory="templates")


class EmailParser:
    def parse(self, email: UploadFile) -> dict:
        file_extension = (
            os.path.splitext(email.filename)[-1].lower().removeprefix(".")
        )  # eml or msg
        if file_extension == "eml":
            return self._parse_eml(email)
        elif file_extension == "msg":
            return self._parse_msg(email)
        else:
            raise ValueError(f"Invalid email type {file_extension}. Use msg or eml")

    def _parse_msg(self, file: UploadFile) -> dict:
        email = {}
        msg = extract_msg.Message(file.file)
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

    def _parse_eml(self, email: UploadFile) -> dict:
        parser = eml_parser.EmlParser(include_raw_body=True, include_attachment_data=True)
        email_bytes = email.file.read()
        parsed_eml = parser.decode_email_bytes(email_bytes)
        return parsed_eml


async def saveUploadFile(in_file: UploadFile):
    # https://stackoverflow.com/a/63581187/15965186
    current_time = datetime.now()
    current_time = current_time.strftime("%Y-%m-%d-%H-%M-%S")
    out_file_path = f"mails/{current_time}_{in_file.filename}"
    print(f"Saving file to {out_file_path}")
    # ...
    async with aiofiles.open(out_file_path, "wb") as out_file:
        while content := await in_file.read(1024):  # async read chunk
            await out_file.write(content)  # async write chunk


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# -------------------------------------------- #


@app.post("/email/parse")
async def parse_email(email: UploadFile):
    try:
        parser = EmailParser()
        return parser.parse(email)
    except ValueError:
        raise HTTPException(status_code=422, detail="File not supported")


@app.post("/email/upload")
async def upload_email(email: UploadFile):
    email.filename = email.filename.replace(" ", "-")
    await saveUploadFile(email)


@app.get("/email/get")
async def get_email(name: str):
    path = f"mails/{name}"
    if not os.path.exists(path):
        return HTTPException(status_code=404, detail=f"File {path} not found")
    return FileResponse(path)


@app.get("/email/list")
async def get_list_email():
    file_list = os.listdir("mails/")
    return file_list


@app.get("/email/all")
async def get_all_email():
    return "To be implemented!"


# -------------------------------------------- #


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
