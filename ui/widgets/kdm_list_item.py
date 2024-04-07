from PyQt6.QtWidgets import QWidget, QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QGridLayout, QTextEdit, QLineEdit
from PyQt6.QtCore import QSize, Qt
from models.kdm_models import Kdm
from ui.dialogs.kdm_dialog import KdmDialog
from ui.widgets.hspacer import HSpacer
from ui.widgets.label import Label

LIST_ITEM_HEIGHT = 95
LIST_ITEM_MARGIN = 15
ITEMS_HORIZONAL_SPACING = 20

class KdmListItem(QWidget):

    def __init__(self, kdm: Kdm, parent=None):
        super().__init__(parent)

        self.kdm = kdm

        layout = QHBoxLayout()
        layout.setContentsMargins(LIST_ITEM_MARGIN, LIST_ITEM_MARGIN, LIST_ITEM_MARGIN, LIST_ITEM_MARGIN)

        email_info_layout = QGridLayout()
        email_info_layout.setHorizontalSpacing(ITEMS_HORIZONAL_SPACING)

        kdm_layout = QVBoxLayout()

        kdm_label = QLabel('KDM')
        kdm_label.setStyleSheet("font-weight: bold;")

        kdm_filename_textedit = QTextEdit()
        kdm_filename_textedit.setText(kdm.filename)
        kdm_filename_textedit.setReadOnly(True)
        kdm_filename_textedit.setDisabled(True)
        kdm_filename_textedit.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        kdm_filename_textedit.setStyleSheet('color: ' + self._get_theme_text_color() + ';')

        kdm_layout.addWidget(kdm_label)
        kdm_layout.addWidget(kdm_filename_textedit)
   

        main_info_layout = QVBoxLayout()
        sender_lineedit = QLineEdit()
        sender_lineedit.setText(kdm.sender)
        sender_lineedit.setReadOnly(True)
        sender_lineedit.setDisabled(True)
        sender_lineedit.setStyleSheet('color: ' + self._get_theme_text_color() + ';')

        subject_lineedit = QLineEdit()
        subject_lineedit.setText(kdm.subject)
        subject_lineedit.setReadOnly(True)
        subject_lineedit.setDisabled(True)
        subject_lineedit.setStyleSheet('color: ' + self._get_theme_text_color() + ';')

        main_info_layout.addWidget(Label(sender_lineedit, "Sender").bold())
        main_info_layout.addWidget(Label(subject_lineedit, "Subject").bold())

        view_kdm_button = QPushButton()
        view_kdm_button.setText("View")
        view_kdm_button.clicked.connect(self.launch_kdm_dialog)

        email_info_layout.addLayout(kdm_layout, 0, 0)
        email_info_layout.addLayout(main_info_layout, 0, 1)

        email_info_layout.setColumnStretch(0, 1)
        email_info_layout.setColumnStretch(1, 1)

        layout.addLayout(email_info_layout)
        layout.addItem(HSpacer(ITEMS_HORIZONAL_SPACING))
        layout.addWidget(view_kdm_button)

        self.setLayout(layout)
        self.setFixedHeight(LIST_ITEM_HEIGHT)

    def sizeHint(self):
        return QSize(0, LIST_ITEM_HEIGHT)

    def _get_theme_text_color(self) -> str:
        return self.palette().text().color().name()

    def launch_kdm_dialog(self):
        kdm_dialog = KdmDialog(self.kdm)
        kdm_dialog.setModal(True)
        kdm_dialog.exec()




