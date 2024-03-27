from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtGui import QPixmap, QDesktopServices
from PyQt6.QtCore import Qt, QUrl
from ui.widgets.hspacer import HSpacer
from ui.widgets.vspacer import VSpacer
from util.file_system_util import get_absolute_path
from util.ui_util import centered

class InfoDialog(QDialog):
    
    def __init__(self):
        super().__init__()

        self.setFixedSize(260, 260)
        self.setWindowTitle("Info")

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        appname_label = QLabel("KDM-Finder (Version 1.0)")

        links_layout = QHBoxLayout()
        links_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        website_link_label = QLabel('<a href="https://www.bdav.dev/code/kdm-finder">Website</a>')
        website_link_label.setOpenExternalLinks(True)
        website_link_label.linkActivated.connect(self.open_link)
       
        github_link_label = QLabel('<a href="https://github.com/bdav-dev/kdm-finder">GitHub</a>')
        github_link_label.setOpenExternalLinks(True)
        github_link_label.linkActivated.connect(self.open_link)

        links_layout.addWidget(website_link_label)
        links_layout.addItem(HSpacer(10))
        links_layout.addWidget(github_link_label)

        logo_label = QLabel()
        logo_pixmap = QPixmap(get_absolute_path(__file__, "..", "..", "assets", "images", "logo.webp")).scaled(128, 128)
        logo_label.setPixmap(logo_pixmap)

        dev_label = QLabel("Developed for FREE CINEMA e.V.")
        author_label = QLabel("David Berezowski (2024)")

        layout.addWidget(centered(logo_label))
        layout.addWidget(centered(appname_label))
        layout.addItem(VSpacer(7))
        layout.addLayout(links_layout)
        layout.addItem(VSpacer(7))
        layout.addWidget(centered(dev_label))
        layout.addWidget(centered(author_label))

        self.setLayout(layout)

    def open_link(self, link):
        QDesktopServices.openUrl(QUrl(link))