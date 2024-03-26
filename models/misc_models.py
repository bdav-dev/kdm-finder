from unittest import skipUnless
from models.email_models import Kdm


class ProgressReporter:

    def __init__(
            self,
            progress_signal
        ):
        self.value: int = 0
        self.max_value: int = 100
        self.progress_signal = progress_signal

    def next(self):
        self.value = self.value + 1
        self._report_progress()

    def _report_progress(self):
        value_from_0_to_100 = (self.value / self.max_value) * 100
        self.progress_signal.emit(int(value_from_0_to_100))

    def clear(self):
        self.progress_signal.emit(0)


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
