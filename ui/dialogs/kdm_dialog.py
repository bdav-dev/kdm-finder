from datetime import date
from typing import Callable, List
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QWidget, QLineEdit, QPushButton, QHBoxLayout, QTextEdit

from models.email_models import Kdm
from models.settings_models import InputValidation, Setting
from storage.persistant_settings import get_settings, set_settings
from ui.dialogs.error_dialog import ErrorDialog
from ui.widgets.hr import Hr
from ui.widgets.hspacer import HSpacer
from ui.widgets.label import Label
from ui.widgets.password_line_edit import PasswordLineEdit
from ui.widgets.vspacer import VSpacer
from util.number_util import is_integer
from util.ui_util import bottom_margin, top_margin



class KdmView(QWidget):

    def __init__(self, kdm: Kdm):
        super().__init__()
        
        sender_lineedit = QLineEdit()
        sender_lineedit.setText(kdm.sender)
        sender_lineedit.setReadOnly(True)

        subject_lineedit = QLineEdit()
        subject_lineedit.setText(kdm.subject)
        subject_lineedit.setReadOnly(True)

        date_lineedit = QLineEdit()
        date_lineedit.setText(kdm.date)
        date_lineedit.setReadOnly(True)

        email_info_layout = QHBoxLayout()
        email_info_layout.addWidget(Label(subject_lineedit, "Subject: "))
        email_info_layout.addItem(HSpacer(5))
        email_info_layout.addWidget(Label(sender_lineedit, "Sender: "))
        email_info_layout.addItem(HSpacer(5))
        email_info_layout.addWidget(Label(date_lineedit, "Date: "))

        email_content_textedit = QTextEdit()
        email_content_textedit.setText(kdm.main_content)
        email_content_textedit.setReadOnly(True)

        attachment_filename_lineedit = QLineEdit()
        attachment_filename_lineedit.setText(kdm.filename)
        attachment_filename_lineedit.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addLayout(email_info_layout)
        layout.addWidget(email_content_textedit)
        layout.addWidget(Label(attachment_filename_lineedit, "Attachment: "))

        self.setLayout(layout)




class KdmDialog(QDialog):
    def __init__(self, kdm: Kdm):
        super().__init__()

        self.setWindowTitle("KDM")

        self.kdm_view = KdmView(kdm)

        self.resize(1300, 500)

        layout = QVBoxLayout()
        layout.addWidget(self.kdm_view)

        self.setLayout(layout)
