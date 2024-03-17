from typing import Callable
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QWidget, QLineEdit, QPushButton, QSpacerItem, QSizePolicy

from models.settings_models import EmailConnectionSettings, Settings
from storage.persistant_settings import get_settings, set_settings
from ui.widgets.hr import Hr
from ui.widgets.label import Label
from ui.widgets.password_line_edit import PasswordLineEdit
from ui.widgets.vspacer import VSpacer
from util.number_util import is_integer
from util.ui_util import bottom_margin, top_margin

ITEMS_SPACING = 5

class SettingsView(QWidget):
    def __init__(self, close_callback: Callable[[], None]):
        super().__init__()

        self.close_callback = close_callback

        label_width = 160

        self.layout = QVBoxLayout()

        self.imap_lineedit = QLineEdit()
        bottom_margin(self.imap_lineedit, ITEMS_SPACING)

        self.email_linedit = QLineEdit()
        bottom_margin(self.email_linedit, ITEMS_SPACING)

        self.password_lineedit = PasswordLineEdit()
        bottom_margin(self.password_lineedit, ITEMS_SPACING)

        self.scan_n_latest_emails_lineedit = QLineEdit()
        bottom_margin(self.scan_n_latest_emails_lineedit, ITEMS_SPACING)

        save_button = QPushButton("Save")
        top_margin(self.scan_n_latest_emails_lineedit, ITEMS_SPACING)
        save_button.clicked.connect(self._save_button_clicked)

        self.layout.addItem(VSpacer())
        self.layout.addWidget(Label(self.imap_lineedit, "IMAP-Server:", label_width))
        self.layout.addWidget(Label(self.email_linedit, "E-Mail:", label_width))
        self.layout.addWidget(Label(self.password_lineedit, "Password:", label_width))
        self.layout.addWidget(Hr())
        self.layout.addWidget(Label(self.scan_n_latest_emails_lineedit, "Scan latest n emails:", label_width))
        self.layout.addItem(VSpacer(15))
        self.layout.addItem(VSpacer())
        self.layout.addWidget(save_button)

        self.setLayout(self.layout)

        self._mount_settings()


    def _input_validation(self) -> bool:
        return self._is_scan_n_latest_emails_numeric()

    def _is_scan_n_latest_emails_numeric(self) -> bool:
        return is_integer(self.scan_n_latest_emails_lineedit.text())

    def _mount_settings(self):
        settings = get_settings()
        self.imap_lineedit.setText(settings.email_connection_settings.imap_server)
        self.email_linedit.setText(settings.email_connection_settings.email_address)
        self.password_lineedit.set_password(settings.email_connection_settings.password)
        self.scan_n_latest_emails_lineedit.setText(str(settings.scan_n_latest_emails))

    def _save_button_clicked(self):
        self._save_settings()
        self.close_callback()

    def _save_settings(self):
        settings = Settings()

        email_connection_settings = EmailConnectionSettings()
        email_connection_settings.imap_server = self.imap_lineedit.text()
        email_connection_settings.email_address = self.email_linedit.text()
        email_connection_settings.password = self.password_lineedit.get_password()
        settings.email_connection_settings = email_connection_settings

        settings.scan_n_latest_emails = self.scan_n_latest_emails_lineedit.text()

        set_settings(settings)

class SettingsDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Settings")

        self.settings = SettingsView(self.close)

        layout = QVBoxLayout()
        layout.addWidget(self.settings)

        self.setLayout(layout)

