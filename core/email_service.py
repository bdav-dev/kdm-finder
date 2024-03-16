import imaplib
import email

from models.settings_models import Email

def get_latest_emails(amount: int) -> list[Email]:
    mail = imaplib.IMAP4_SSL()
