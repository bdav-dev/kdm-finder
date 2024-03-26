
from PyQt6.QtWidgets import QWidget, QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QLineEdit

from models.email_models import Kdm
from ui.dialogs.kdm_dialog import KdmDialog

class KdmListItem(QWidget):

    def __init__(self, kdm: Kdm, parent=None):
        super().__init__(parent)

        self.kdm = kdm

        layout = QHBoxLayout()

        main_info = QWidget()
        main_info_layout = QVBoxLayout()
        main_info.setLayout(main_info_layout)
        
        sender_label = QLabel()
        sender_label.setText("Sender: " + kdm.sender)

        subject_label = QLabel()
        subject_label.setText("Subject: " + kdm.subject)

        main_info_layout.addWidget(sender_label)
        main_info_layout.addWidget(subject_label)

        filename_label = QLabel()
        filename_label.setText(kdm.filename)

        layout.addWidget(filename_label)

        layout.addStretch()

        layout.addWidget(main_info)

        layout.addStretch()

        view_kdm_button = QPushButton()
        view_kdm_button.setText("View")
        view_kdm_button.clicked.connect(self.launch_kdm_dialog)


        layout.addWidget(view_kdm_button)

        self.setLayout(layout)

    def launch_kdm_dialog(self):
        kdm_dialog = KdmDialog(self.kdm)
        kdm_dialog.setModal(True)
        kdm_dialog.exec()




