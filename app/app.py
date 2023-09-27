from fastapi import FastAPI, Request, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
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


def parse_msg(file: UploadFile) -> dict:
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


def parse_eml(email: UploadFile) -> dict:
    parser = eml_parser.EmlParser(
        include_raw_body=True, include_attachment_data=True, ignore_bad_start=True
    )
    email_bytes = email.file.read()
    parsed_eml = parser.decode_email_bytes(email_bytes)
    return parsed_eml


def standarize_email_response(email: dict, type) -> dict:
    # FIXME: This should not be done like this, consider implementing something with pydantic :P
    if type == ".msg":
        pass
    if type == ".eml":
        pass
    else:
        raise TypeError(f"type {type} not supported")


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


@app.post("/email-info")
async def get_email_info(email: UploadFile):
    email.filename = email.filename.replace(" ", "-")
    file_extension = os.path.splitext(email.filename)[-1].lower()
    if file_extension == ".msg":
        parsedEmail = parse_msg(email)
    elif file_extension == ".eml":
        parsedEmail = parse_eml(email)
    else:
        raise HTTPException(status_code=422, detail="File not supported")
    # standarize_email_response(parsedEmail, type=file_extension)
    # ! THIS SHOULD BE CALLED AFTER THE PARSING. If done otherwise, the file saving will delete the content
    await saveUploadFile(email)
    print(parsedEmail)
    return parsedEmail


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
