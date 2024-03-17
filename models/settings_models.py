
class EmailConnectionSettings:
    def __init__(
            self,
            imap_server: str = None,
            email_address: str = None,
            password: str = None
        ):
        self.imap_server = imap_server
        self.email_address = email_address
        self.password = password

class Settings:
    def __init__(
            self,
            email_connection_settings: EmailConnectionSettings = EmailConnectionSettings(),
            scan_n_latest_emails: int = 50
        ):
        self.email_connection_settings = email_connection_settings
        self.scan_n_latest_emails = scan_n_latest_emails

