from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QListWidget, QProgressBar, QHBoxLayout, QLabel

from ui.dialogs.info_dialog import InfoDialog
from ui.dialogs.settings_dialog import SettingsDialog

class KdmFinderView(QWidget):

    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout()
        self.setLayout(layout)

        button = QPushButton("Click")
        button.clicked.connect(self.launch_settings_dialog)

        self.kdm_list = QListWidget()
        self.kdm_list.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)

        progressbar = QProgressBar()
        progressbar.setFixedHeight(7)
        progressbar.setRange(0, 0)


        top_bar = QWidget()
        top_bar_layout = QHBoxLayout()
        top_bar.setLayout(top_bar_layout)

        top_bar_layout.addWidget(QLabel("KDMs"))
        top_bar_layout.setContentsMargins(0, 0, 0, 0)
        
        refresh_kdm_list_button = QPushButton("Refresh")
        refresh_kdm_list_button.setFixedWidth(70)
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
        layout.addWidget(progressbar)
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


def launch():
    app = QApplication([])

    window = QMainWindow()
    window.setMinimumSize(400, 300)
    window.setBaseSize(900, 700)
    window.setWindowTitle("KDM-Finder")

    window.setCentralWidget(KdmFinderView())

    screen_geometry = app.primaryScreen().geometry()
    center_point = screen_geometry.center()
    top_left = center_point - window.rect().center()

    window.move(top_left)

    window.show()
    app.exec()
