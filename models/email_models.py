from email.message import Message


class Attachment:

    def __init__(
            self,
            filename: str,
            part: Message
        ):
        self.filename = filename
        self.part = part



class Email:
    
    def __init__(self):
        self.sender: str = None
        self.subject: str = None
        self.date: str = None
        self.main_content: str = None
        self.attachments: list[Attachment] = []


    def append_main_content(self, main_content: str):
        if not main_content or not isinstance(main_content, str):
            return

        if (self.main_content == None or self.main_content == ''):
            self.main_content = main_content
        else:
            self.main_content += "\n" + main_content
