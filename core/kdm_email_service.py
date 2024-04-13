import email.header
from email.message import Message
import imaplib
import email
from typing import Callable

from models.email_models import Attachment, Email
from models.kdm_models import Kdm, KdmFetchResponse
from models.misc_models import ProgressReporter
from models.settings_models import EmailConnectionSettings

def _establish_email_connection(email_connection_settings: EmailConnectionSettings) -> imaplib.IMAP4_SSL:
    email_connection: imaplib.IMAP4_SSL
    
    try: 
        email_connection = imaplib.IMAP4_SSL(email_connection_settings.imap_server)
        email_connection.login(email_connection_settings.email_address, email_connection_settings.password)
        email_connection.select('INBOX')

    except Exception as e:
        raise Exception("Connection to email server couldn't be established. Please verify your email connection settings.\n\nException: " + str(e))

    return email_connection


def _fetch_latest_emails_raw(
        scan_n_latest_emails: int,
        email_connection: imaplib.IMAP4_SSL
    ):
    status, raw_mail_data = email_connection.search(None, 'ALL')

    if status.lower() != 'ok':
        raise Exception("Error while fetching latest emails. Status: " + status)
    
    latest_emails: list[any] = raw_mail_data[0].split()[-scan_n_latest_emails:]
    latest_emails.reverse()

    return latest_emails


def _convert_raw_emails(
        latest_emails,
        email_connection: imaplib.IMAP4_SSL,
        progress_reporter: ProgressReporter = None
    ) -> tuple[list[str], list[Email]]:
    emails: list[Email] = []
    skipped_emails: list[str] = []
    
    if progress_reporter:
        progress_reporter.max_value = len(latest_emails)

    for num in latest_emails:
        status, raw_mail_data = email_connection.fetch(num, '(RFC822)')

        if status.lower() == 'ok':
            mail_data = email.message_from_bytes(raw_mail_data[0][1])
            mail = _get_mail_object(mail_data)
            emails.append(mail)
        else:
            skipped_emails.append(str(num) + ", Status: " + status)

        if progress_reporter:
            progress_reporter.next()

    return (skipped_emails, emails)


def _decode_subject(encoded_subject) -> str:
    decoded_subject = ""

    for part, encoding in email.header.decode_header(encoded_subject):
        if isinstance(part, bytes):
            if encoding == None:
                decoded_subject += part.decode('utf-8', errors='replace')
            else:
                decoded_subject += part.decode(encoding, errors='replace')
                
        elif isinstance(part, str):
            decoded_subject += part
    
    return decoded_subject


def _get_mail_object(mail_data: Message) -> Email:
    mail = Email()

    mail.subject = _decode_subject(mail_data['Subject'])
    mail.sender = mail_data['From']
    mail.date = mail_data['Date']

    for part in mail_data.walk():
        filename = part.get_filename()
        if filename:
            mail.attachments.append(Attachment(filename, part))
        else:
            content = part.get_payload(decode=True)
            charset = part.get_content_charset()

            if content:
                if charset: content = content.decode(charset)
                mail.append_main_content(content)
    
    return mail


def _close_email_connection(email_connection: imaplib.IMAP4_SSL):
    email_connection.close()
    email_connection.logout()


def _get_kdms_from_emails(mails: list[Email]) -> list[Kdm]:
    kdms: list[Kdm] = []

    for mail in mails:
        kdms.extend(_get_kdm_from_email(mail))

    return kdms


def _get_kdm_from_email(mail: Email) -> list[Kdm]:
    kdms: list[Kdm] = []
    
    KEYWORDS = ['kdm', 'key']
    FIND_KEYWORD_IN: list[Callable[[], str]] = [
        lambda: mail.main_content,
        lambda: mail.sender,
        lambda: mail.subject
    ]
    FIND_KEYWORD_IN.extend(map(lambda attachment: lambda: attachment.filename, mail.attachments))

    VALID_ATTACHMENT_FILE_EXTENSIONS = ['.zip', '.xml']

    if not mail.attachments:
        return []
    
    does_mail_contain_keyword = any(
        keyword in ('' if text() == None else text().lower()) for keyword in KEYWORDS for text in FIND_KEYWORD_IN
    )
    if not does_mail_contain_keyword:
        return []
    
    for attachment in mail.attachments:
        is_valid_extension = any(
            attachment.filename.lower().endswith(extension) for extension in VALID_ATTACHMENT_FILE_EXTENSIONS
        )
        if not is_valid_extension:
            continue

        kdms.append(
            Kdm(
                sender=mail.sender,
                subject=mail.subject,
                date=mail.date,
                main_content=mail.main_content,
                filename=attachment.filename,
                file=attachment.part.get_payload(decode=True)
            )
        )

    return kdms


def get_kdms_from_email(
        email_connection_settings: EmailConnectionSettings,
        scan_n_latest_emails: int,
        progress_reporter: ProgressReporter = None
    ) -> KdmFetchResponse:

    skipped_emails: list[str]
    kdms: list[Kdm]

    try:
        email_connection = _establish_email_connection(email_connection_settings)
        latest_emails_raw = _fetch_latest_emails_raw(scan_n_latest_emails, email_connection)

        skipped_emails, emails = _convert_raw_emails(latest_emails_raw, email_connection, progress_reporter)

        kdms = _get_kdms_from_emails(emails)
        _close_email_connection(email_connection)

    except Exception as e:
        return KdmFetchResponse.erroneous(str(e))

    return KdmFetchResponse.from_response(kdms, skipped_emails)
