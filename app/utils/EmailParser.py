from tempfile import SpooledTemporaryFile
import extract_msg
import eml_parser
import os


class EmailParser:
    @staticmethod
    def parse(email: SpooledTemporaryFile, filename: str) -> dict:
        file_extension = os.path.splitext(filename)[-1].lower().removeprefix(".")  # eml or msg
        if file_extension == "eml":
            return EmailParser._parse_eml(email)
        elif file_extension == "msg":
            return EmailParser._parse_msg(email)
        else:
            raise ValueError(f"Invalid email type {file_extension}. Use msg or eml")

    @staticmethod
    def _parse_msg(file: SpooledTemporaryFile) -> dict:
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

    @staticmethod
    def _parse_eml(email: SpooledTemporaryFile) -> dict:
        parser = eml_parser.EmlParser(include_raw_body=True, include_attachment_data=True)
        eml_bytes = email.read()
        parsed_eml = parser.decode_email_bytes(eml_bytes)
        return parsed_eml
