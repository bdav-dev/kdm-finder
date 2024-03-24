from tkinter import W
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QListWidget, QProgressBar, QHBoxLayout, QLabel

from core.email_service import get_kdms_from_email
from models.misc_models import ProgressReporter
from storage.persistant_settings import get_settings
from ui.dialogs.info_dialog import InfoDialog
from ui.dialogs.settings_dialog import SettingsDialog
from util.ui_async import Async

class KdmFinderView(QWidget):

    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.kdm_list = QListWidget()
        self.kdm_list.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)

        self.progressbar = QProgressBar()
        self.progressbar.setFixedHeight(7)
        self.progressbar.setRange(0, 100)
        self.progressbar.setValue(0)
        self.progressbar.setTextVisible(False)


        top_bar = QWidget()
        top_bar_layout = QHBoxLayout()
        top_bar.setLayout(top_bar_layout)

        top_bar_layout.addWidget(QLabel("KDMs"))
        top_bar_layout.setContentsMargins(0, 0, 0, 0)
        
        refresh_kdm_list_button = QPushButton("Refresh")
        refresh_kdm_list_button.setFixedWidth(70)
        refresh_kdm_list_button.clicked.connect(self.refresh_button_clicked)
        top_bar_layout.addWidget(refresh_kdm_list_button)

        buttons_bar = QWidget()
        buttons_bar_layout = QHBoxLayout()
        buttons_bar.setLayout(buttons_bar_layout)

        save_selected_button = QPushButton("Save selected")
        buttons_bar_layout.addWidget(save_selected_button)

        copy_selected_to_usb_button = QPushButton("Copy selected to USB media")
        buttons_bar_layout.addWidget(copy_selected_to_usb_button)

        settings_bar = QWidget()
        settings_bar_layout = QHBoxLayout()
        settings_bar.setLayout(settings_bar_layout)

        settings_button = QPushButton("Settings")
        settings_button.setFixedWidth(100)
        settings_button.clicked.connect(self.launch_settings_dialog)
        settings_bar_layout.addWidget(settings_button)

        settings_bar_layout.addStretch()

        info_button = QPushButton("Info")
        info_button.setFixedWidth(40)
        info_button.clicked.connect(self.launch_info_dialog)
        settings_bar_layout.addWidget(info_button)

        layout.addWidget(top_bar)
        layout.addWidget(self.kdm_list)
        layout.addWidget(self.progressbar)
        layout.addWidget(buttons_bar)
        layout.addWidget(settings_bar)

    def launch_settings_dialog(self):
        settings_dialog = SettingsDialog()
        settings_dialog.setModal(True)
        settings_dialog.exec()

    def launch_info_dialog(self):
        info_dialog = InfoDialog()
        info_dialog.setModal(True)
        info_dialog.exec()

    def refresh_button_clicked(self):
        settings = get_settings()

        progress_reporter = ProgressReporter(lambda value: self.progressbar.setValue(int(value)))
        progress_reporter.clear()

        self.thread = Async(
            run_async=lambda: get_kdms_from_email(settings.email_connection_settings, settings.scan_n_latest_emails, progress_reporter),
            when_done=lambda kdms: self.test(kdms)
        )

    def test(self, res):
        print("done")


def launch():
    app = QApplication([])

    window = QMainWindow()
    window.setMinimumSize(400, 300)
    window.resize(900, 500)
    window.setWindowTitle("KDM-Finder")

    window.setCentralWidget(KdmFinderView())

    screen_geometry = app.primaryScreen().geometry()
    center_point = screen_geometry.center()
    top_left = center_point - window.rect().center()

    window.move(top_left)

    window.show()
    app.exec()
