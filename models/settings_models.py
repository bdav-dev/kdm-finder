from typing import Callable


class InputValidation:

    def __init__(self, reject_reason: str = None):
        self.reject_reason = reject_reason


    @staticmethod
    def accept():
        return InputValidation()
    

    @staticmethod
    def reject(reject_reason: str):
        return InputValidation(reject_reason)


    def was_accepted(self):
        return self.reject_reason == None
    

    def was_rejected(self):
        return self.reject_reason != None



class Setting:
    def __init__(
            self,
            default_value: any,
            value_supplier: Callable[[], any],
            value_emit_consumer: Callable[[any], None],
            validation: Callable[[str], InputValidation],
    ):
        self.default_value = default_value
        self._value_supplier = value_supplier
        self._value_emit_consumer = value_emit_consumer
        self._validation = validation


    def emit(self):
        self._value_emit_consumer(self._value_supplier())


    def validate(self) -> InputValidation:
        return self._validation(self._value_supplier())



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


    def set_imap_server(self, imap_server):
        self.imap_server = imap_server


    def set_email_address(self, email_address):
        self.email_address = email_address


    def set_password(self, password):
        self.password = password



class Settings:
    def __init__(
            self,
            email_connection_settings: EmailConnectionSettings = EmailConnectionSettings(),
            scan_n_latest_emails: int = 50
        ):
        self.email_connection_settings = email_connection_settings
        self.scan_n_latest_emails = scan_n_latest_emails


    def set_scan_n_latest_emails(self, scan_n_latest_emails):
        self.scan_n_latest_emails = scan_n_latest_emails