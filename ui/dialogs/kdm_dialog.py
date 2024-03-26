from PyQt6.QtWidgets import QDialog, QVBoxLayout, QWidget, QLineEdit, QHBoxLayout, QTextEdit

from models.kdm_models import Kdm
from ui.widgets.hspacer import HSpacer
from ui.widgets.label import Label

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

        self.resize(1300, 600)

        layout = QVBoxLayout()
        layout.addWidget(self.kdm_view)

        self.setLayout(layout)
