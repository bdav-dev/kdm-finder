from tkinter import W
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QListWidget, QProgressBar, QHBoxLayout, QLabel, QListWidgetItem
from PyQt6.QtGui import QIcon, QPixmap

import os

from core.email_service import get_kdms_from_email
from models.email_models import Kdm
from models.misc_models import ProgressReporter
from storage.persistant_settings import get_settings
from ui.dialogs.info_dialog import InfoDialog
from ui.dialogs.settings_dialog import SettingsDialog
from ui.widgets.kdm_list_item import KdmListItem
from util.ui_async import Async

class KdmFinderView(QWidget):

    def __init__(self):
        super().__init__()

        self.blockable_widgets = []

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.kdm_list = QListWidget()
        self.kdm_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)

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
        self.blockable_widgets.append(refresh_kdm_list_button)

        buttons_bar = QWidget()
        buttons_bar_layout = QHBoxLayout()
        buttons_bar.setLayout(buttons_bar_layout)

        save_selected_button = QPushButton("Save selected")
        self.blockable_widgets.append(save_selected_button)
        buttons_bar_layout.addWidget(save_selected_button)
        
        copy_selected_to_usb_button = QPushButton("Copy selected to USB media")
        self.blockable_widgets.append(copy_selected_to_usb_button)
        buttons_bar_layout.addWidget(copy_selected_to_usb_button)

        settings_bar = QWidget()
        settings_bar_layout = QHBoxLayout()
        settings_bar.setLayout(settings_bar_layout)

        settings_button = QPushButton("Settings")
        settings_button.setFixedWidth(100)
        settings_button.clicked.connect(self.launch_settings_dialog)
        self.blockable_widgets.append(settings_button)
        settings_bar_layout.addWidget(settings_button)

        settings_bar_layout.addStretch()

        info_button = QPushButton("Info")
        info_button.setFixedWidth(40)
        info_button.clicked.connect(self.launch_info_dialog)
        self.blockable_widgets.append(info_button)
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

        self.kdm_list.clear()
        self.progressbar.setValue(0)
        self.set_widgets_blocked(True)

        self.async_operation = Async(
            run_async=lambda progress_signal: get_kdms_from_email(settings.email_connection_settings, settings.scan_n_latest_emails, ProgressReporter(progress_signal)),
            when_done=lambda kdms: self.handle_response(kdms),
            progress=lambda progress: self.progressbar.setValue(progress)
        )

    def handle_response(self, kdms: list[Kdm]):
        print("done")
        self.set_widgets_blocked(False)

        for kdm in kdms:
            item = QListWidgetItem(self.kdm_list)
            kdm_list_item = KdmListItem(kdm)
            item.setSizeHint(kdm_list_item.sizeHint())
            self.kdm_list.setItemWidget(item, kdm_list_item)


    def set_widgets_blocked(self, blocked: bool):
        for widget in self.blockable_widgets:
            widget.setDisabled(blocked)

def launch():
    app = QApplication([])

    window = QMainWindow()
    window.setMinimumSize(400, 300)
    window.resize(900, 500)
    window.setWindowTitle("KDM-Finder")
    window.setWindowIconText("KDM-Finder")

    window.setCentralWidget(KdmFinderView())
    
    path = os.path.dirname(os.path.abspath(__file__))
    logo_pixmap = QPixmap(os.path.join(path, "../assets/images/logo.webp"))

    app.setApplicationName("KDM-Finder")
    app.setApplicationDisplayName("KDM-Finder")
    app.setWindowIcon(QIcon(logo_pixmap))

    screen_geometry = app.primaryScreen().geometry()
    center_point = screen_geometry.center()
    top_left = center_point - window.rect().center()

    window.move(top_left)

    window.show()
    app.exec()
