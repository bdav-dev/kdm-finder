from typing import Callable, List
from PyQt6.QtGui import QCloseEvent
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QWidget, QLineEdit, QPushButton

from models.settings_models import InputValidation, Setting
from core.settings_service import get_settings, set_settings
from ui.dialogs.error_dialog import ErrorDialog
from ui.widgets.hr import Hr
from ui.widgets.label import Label
from ui.widgets.password_line_edit import PasswordLineEdit
from ui.widgets.vspacer import VSpacer
from util.number_util import is_integer
from util.string_util import enumerate
from util.ui_util import bottom_margin, top_margin


class SettingsView(QWidget):
    
    def __init__(self, close_callback: Callable[[], None]):
        super().__init__()

        self.close_callback = close_callback
        self.settings = get_settings()
        
        self._init_ui()
        self._init_setting_values()
        self._mount_settings()


    def _init_ui(self):
        label_width = 160
        items_spacing = 5

        self.layout = QVBoxLayout()

        self.imap_lineedit = QLineEdit()
        bottom_margin(self.imap_lineedit, items_spacing)

        self.email_linedit = QLineEdit()
        bottom_margin(self.email_linedit, items_spacing)

        self.password_lineedit = PasswordLineEdit()
        bottom_margin(self.password_lineedit, items_spacing)

        self.scan_n_latest_emails_lineedit = QLineEdit()
        bottom_margin(self.scan_n_latest_emails_lineedit, items_spacing)

        save_button = QPushButton("Save")
        top_margin(self.scan_n_latest_emails_lineedit, items_spacing)
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


    def _init_setting_values(self):
        self.setting_values: List[Setting] = []

        self.imap_server_setting = Setting(
            default_value=self.settings.email_connection_settings.imap_server,
            value_supplier=lambda: self.imap_lineedit.text(),
            value_emit_consumer=lambda value: self.settings.email_connection_settings.set_imap_server(value),
            validation=lambda value: (
               InputValidation.reject("IMAP server is not specified") if value.isspace() or not value  else InputValidation.accept()
            )
        )
        self.setting_values.append(self.imap_server_setting)

        self.email_address_setting = Setting(
            default_value=self.settings.email_connection_settings.email_address,
            value_supplier=lambda: self.email_linedit.text(),
            value_emit_consumer=lambda value: self.settings.email_connection_settings.set_email_address(value),
            validation=lambda value: (
               InputValidation.reject("Email is not specified") if value.isspace() or not value else InputValidation.accept()
            )
        )
        self.setting_values.append(self.email_address_setting)

        self.password_setting = Setting(
            default_value=self.settings.email_connection_settings.password,
            value_supplier=lambda: self.password_lineedit.get_password(),
            value_emit_consumer=lambda value: self.settings.email_connection_settings.set_password(value),
            validation=lambda value: (
               InputValidation.reject("Password is not specified") if value.isspace() or not value  else InputValidation.accept()
            )
        )
        self.setting_values.append(self.password_setting)

        self.scan_n_latest_emails_setting = Setting(
            default_value=self.settings.scan_n_latest_emails,
            value_supplier=lambda: self.scan_n_latest_emails_lineedit.text(),
            value_emit_consumer=lambda value: self.settings.set_scan_n_latest_emails(int(value)),
            validation=lambda value: self.validate_scan_n_latest_emails(value)
        )
        self.setting_values.append(self.scan_n_latest_emails_setting)


    def _mount_settings(self):
        self.imap_lineedit.setText(self.imap_server_setting.default_value)
        self.email_linedit.setText(self.email_address_setting.default_value)
        self.password_lineedit.set_password(self.password_setting.default_value)
        self.scan_n_latest_emails_lineedit.setText(str(self.scan_n_latest_emails_setting.default_value))


    def _save_button_clicked(self):
        self._save_settings()


    def _save_settings(self):
        reject_reasons: List[str] = []

        for setting in self.setting_values:
            input_validation = setting.validate()

            if input_validation.was_rejected():
                reject_reasons.append(input_validation.reject_reason)


        if reject_reasons:
            self.show_input_validation_error_dialog(reject_reasons)

        else:
            for setting in self.setting_values:
                setting.emit()

            set_settings(self.settings)
            self.close_callback()
            

    def validate_scan_n_latest_emails(self, user_input: str):
        if user_input.isspace() or not user_input:
            return InputValidation.reject("Scan n latest emails is not specified")

        if not is_integer(user_input):
            return InputValidation.reject("Scan n latest emails must be an integer")
        
        value_as_int = int(user_input)

        if value_as_int <= 0:
            return InputValidation.reject("Scan n latest emails must be positive")

        return InputValidation.accept()


    def show_input_validation_error_dialog(self, reject_reasons):
        input_validation_error_message = "Some of your inputs are empty or incorrect.\nPlease check the following error messages:\n\n"

        dialog = ErrorDialog(
            "Input validation error",
            input_validation_error_message + enumerate(reject_reasons)
        )
        dialog.setModal(True)
        dialog.exec()


class SettingsDialog(QDialog):

    def __init__(self, exit_app_on_close: bool = False):
        super().__init__()

        self.exit_app_on_close = exit_app_on_close

        self.setWindowTitle("Settings")
        self.setFixedHeight(250)

        self.settings = SettingsView(self.close)

        layout = QVBoxLayout()
        layout.addWidget(self.settings)

        self.setLayout(layout)


    def closeEvent(self, event: QCloseEvent | None) -> None:
        is_window_bar_close = False if not event else event.spontaneous()

        if is_window_bar_close:
            if not self.exit_app_on_close:
                event.accept()
            else:
                exit()
        else:
            event.accept()

