
class Kdm:

    def __init__(
            self,
            sender: str,
            subject: str,
            date: str,
            main_content: str,
            filename: str,
            file
        ):
        self.sender = sender
        self.subject = subject
        self.date = date
        self.main_content = main_content
        self.filename = filename
        self.file = file



class KdmFetchResponse:

    def __init__(
            self,
            kdms: list[Kdm] = None,
            error_message: str = None,
            skipped_emails: list[str] = None 
        ):
        self.kdms = kdms
        self.error_message = error_message
        self.skipped_emails = skipped_emails


    @classmethod
    def from_response(cls, kdms: list[Kdm], skipped_emails: list[str] = None):
        return cls(
            kdms=kdms,
            skipped_emails=skipped_emails
        )


    @classmethod
    def erroneous(cls, error_message: str):
        return cls(error_message=error_message)


    def is_erroneous(self) -> bool:
        return self.error_message != None
    

    def has_response(self) -> bool:
        if self.kdms is None:
            return False
        
        if not self.kdms:
            return False
        
        return True
    

    def has_skipped_emails(self) -> bool:
        if self.skipped_emails is None:
            return False
        
        if not self.skipped_emails:
            return False
        
        return True
