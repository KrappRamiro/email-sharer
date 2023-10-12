class Email:
    def __init__(
        self,
        subject: str,
        sender: str,
        recipients: str,
        cc: str | None,
        bcc: str | None,
        date: str,
        body: str,
        attachments: list,
        filename: str,
    ) -> None:
        self.subject = (subject,)
        self.sender = (sender,)
        self.recipients = (recipients,)
        self.cc = cc
        self.bcc = bcc
        self.date = (date,)
        self.body = body
        self.filename = filename
