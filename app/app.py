from fastapi import FastAPI, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import extract_msg
import eml_parser
import datetime
import json


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/static/css", StaticFiles(directory="static/css"), name="css")
app.mount("/static/img", StaticFiles(directory="static/img"), name="img")
app.mount("/static/js", StaticFiles(directory="static/js"), name="js")
templates = Jinja2Templates(directory="templates")

def json_serial(obj):
  if isinstance(obj, datetime.datetime):
      serial = obj.isoformat()
      return serial


def get_msg(file: UploadFile):
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
        attachments.append(attachment.filename)
    email["attachments"] = attachments
    return email

def get_eml(email: UploadFile):
        parser = eml_parser.EmlParser(include_raw_body=True, include_attachment_data=True)
        email_bytes = email.file.read()
        parsed_eml = parser.decode_email_bytes(email_bytes)
        return parsed_eml



@app.post("/file-info")
async def get_file_info(email: UploadFile):
    if email.filename.endswith(".msg"):
        return get_msg(email)
    elif email.filename.endswith(".eml"):
        return get_eml(email)



@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
   return templates.TemplateResponse("index.html", {"request": request})
