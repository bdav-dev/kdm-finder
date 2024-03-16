
class Attachment:
    def __init__(self, filename: str, data):
        self.filename = filename
        self.data = data

class Email:
    def __init__(
            self,
            subject: str,
            sender: str,
            main_content: str,
            attachments: list[Attachment]
        ):
        self.subject = subject
        self.sender = sender
        self.main_content = main_content
        self.attachments = attachments