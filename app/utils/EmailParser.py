from tempfile import SpooledTemporaryFile
import extract_msg
import eml_parser
import os
from sql_app import schemas
from email.utils import parseaddr


class EmailParser:
    @staticmethod
    def parse(email: SpooledTemporaryFile, filename: str) -> dict:
        file_extension = os.path.splitext(filename)[-1].lower().removeprefix(".")  # eml or msg
        if file_extension == "eml":
            return EmailParser._parse_eml(email, filename)
        elif file_extension == "msg":
            return EmailParser._parse_msg(email, filename)
        else:
            raise ValueError(f"Invalid email type {file_extension}. Use msg or eml")

    @staticmethod
    def _parse_msg(file: SpooledTemporaryFile, filename: str) -> dict:
        email = {}

        msg = extract_msg.Message(file)
        email["subject"] = msg.subject
        email["sender"] = msg.sender
        email["recipients"] = msg.to
        email["cc"] = msg.cc
        email["bcc"] = msg.bcc
        email["date"] = msg.date
        email["body"] = msg.body
        email["filename"] = filename
        attachments = []
        for attachment in msg.attachments:
            attachments.append(attachment.getFilename())
        email["attachments"] = attachments
        return schemas.EmailBase(**email)

    @staticmethod
    def _parse_eml(email: SpooledTemporaryFile, filename: str) -> dict:
        parser = eml_parser.EmlParser(include_raw_body=True, include_attachment_data=True)
        eml_bytes = email.read()
        parsed_eml = parser.decode_email_bytes(eml_bytes)
        email = {
            "subject": parsed_eml["header"]["subject"],
            "sender": parseaddr(parsed_eml["header"]["from"])[1],
            "recipients": parseaddr(parsed_eml["header"]["to"])[1],
            "cc": parsed_eml["header"]["cc"],
            "bcc": parsed_eml["header"]["bcc"],
            "date": parsed_eml["header"]["date"],
            "body": parsed_eml["body"],
            "filename": filename,
            "attachments": [
                schemas.AttachmentBase(filename=attachment["filename"])
                for attachment in parsed_eml.get("attachments", [])
            ],
        }
        return schemas.EmailBase(**email)
