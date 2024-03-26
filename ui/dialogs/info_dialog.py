from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from util.file_system_util import get_absolute_path
from util.ui_util import centered

class InfoDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setFixedSize(260, 260)
        self.setWindowTitle("Info")

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        app_label = QLabel("KDM-Finder (Version 1.0)")
        app_label.setContentsMargins(0, 0, 0, 10)

        logo_label = QLabel()
       
        logo_pixmap = QPixmap(get_absolute_path(__file__, "..", "..", "assets", "images", "logo.webp")).scaled(128, 128)
        logo_label.setPixmap(logo_pixmap)

        dev_label = QLabel("Developed for FREE CINEMA e.V.")
        author_label = QLabel("David Berezowski (2024)")

        layout.addWidget(centered(logo_label))
        layout.addWidget(centered(app_label))
        layout.addWidget(centered(dev_label))
        layout.addWidget(centered(author_label))

        self.setLayout(layout)