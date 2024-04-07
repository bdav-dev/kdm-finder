import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QListWidget, QProgressBar, QHBoxLayout, QLabel, QListWidgetItem, QFileDialog, QMenu
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon, QPixmap, QAction

from core.kdm_email_service import get_kdms_from_email
from core.save_kdm_service import save_kdms
from models.kdm_models import Kdm, KdmFetchResponse
from models.misc_models import ProgressReporter
from core.settings_service import are_kdm_fetch_settings_valid, get_settings
from ui.dialogs.error_dialog import ErrorDialog
from ui.dialogs.info_dialog import InfoDialog
from ui.dialogs.kdm_fetch_error_dialog import KdmFetchErrorDialog
from ui.dialogs.settings_dialog import SettingsDialog
from ui.dialogs.success_dialog import SuccessDialog
from ui.widgets.kdm_list_item import KdmListItem
from ui.widgets.vspacer import VSpacer
from util.file_system_util import get_absolute_path
from util.ui_async import Async
from util.string_util import enumerate


class KdmFinderView(QWidget):

    def __init__(self):
        super().__init__()

        self.blockable_widgets: list[QWidget] = []

        layout = QVBoxLayout()
        self.setLayout(layout)

        top_bar_layout = QHBoxLayout()
        top_bar_layout.setContentsMargins(0, 0, 0, 0)

        top_bar_layout.addWidget(QLabel("KDMs"))
        
        refresh_kdm_list_button = QPushButton("Refresh")
        refresh_kdm_list_button.setFixedWidth(70)
        refresh_kdm_list_button.clicked.connect(self.refresh_button_clicked)
        top_bar_layout.addWidget(refresh_kdm_list_button)
        self.blockable_widgets.append(refresh_kdm_list_button)

        self.kdm_list = QListWidget()
        self.kdm_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.kdm_list.customContextMenuRequested.connect(self._show_list_item_context_menu)
        self.kdm_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)

        self.progressbar = QProgressBar()
        self.progressbar.setFixedHeight(8)
        self.progressbar.setRange(0, 100)
        self.progressbar.setValue(0)
        self.progressbar.setTextVisible(False)

        self.save_selected_button = QPushButton("Save selected")
        self.save_selected_button.clicked.connect(self.save_selected_button_clicked)
        self.blockable_widgets.append(self.save_selected_button)

        settings_bar_layout = QHBoxLayout()

        settings_button = QPushButton("Settings")
        settings_button.setFixedWidth(100)
        settings_button.clicked.connect(self.launch_settings_dialog)
        settings_bar_layout.addWidget(settings_button)

        settings_bar_layout.addStretch()

        info_button = QPushButton("Info")
        info_button.setFixedWidth(40)
        info_button.clicked.connect(self.launch_info_dialog)
        settings_bar_layout.addWidget(info_button)

        layout.addLayout(top_bar_layout)
        layout.addWidget(self.kdm_list)
        layout.addWidget(self.progressbar)
        layout.addItem(VSpacer(5))
        layout.addWidget(self.save_selected_button)
        layout.addItem(VSpacer(25))
        layout.addLayout(settings_bar_layout)

        self.init()


    def init(self):
        self.save_selected_button.setEnabled(False)

        if not are_kdm_fetch_settings_valid():
            self.launch_settings_dialog(True)
        
        if get_settings().fetch_kdms_on_app_startup:
            self.refresh_kdms()

    
    def _show_list_item_context_menu(self, pos):
        if self.kdm_list.count() == 0:
            return

        item_clicked_on = self.kdm_list.itemAt(pos)
        kdm_clicked_on: Kdm = None

        if item_clicked_on:
            kdm_clicked_on = self.kdm_list.itemWidget(item_clicked_on).kdm

        menu = QMenu(self)

        if kdm_clicked_on != None:
            save_action = QAction("Save single", self)
            save_action.triggered.connect(lambda: self.save_kdms([kdm_clicked_on]))
            menu.addAction(save_action)

        save_selected_action = QAction("Save selected", self)
        save_selected_action.triggered.connect(self.save_selected_kdms)
        menu.addAction(save_selected_action)

        menu.exec(self.kdm_list.mapToGlobal(pos))


    def save_selected_button_clicked(self):
        self.save_selected_kdms()


    def save_selected_kdms(self):
        selected_items = self.kdm_list.selectedItems()

        if not selected_items:
            self.launch_error_dialog("Save error", "No items selected.", QSize(310, 210))
            return
        
        selected_kdms: list[Kdm] = list(map(lambda selected: self.kdm_list.itemWidget(selected).kdm, selected_items))

        self.save_kdms(selected_kdms)
    

    def save_kdms(self, kdms: list[Kdm]):
        home_dir = os.path.expanduser("~")
        destination_dir = QFileDialog.getExistingDirectory(self, "Select Save Directory", home_dir)
        
        if not destination_dir:
            return

        try:
            save_kdms(kdms, destination_dir)
            self.launch_success_dialog(
                "Successfully saved",
                "Successfully saved following file(s):" + "\n" +
                enumerate(
                    map(lambda kdm: "Contents of " + kdm.filename if kdm.filename.lower().endswith(".zip") else kdm.filename, kdms)
                ) + "\n" +
                "to " + destination_dir
            )
        except Exception as e:
            self.launch_error_dialog("Save error", "File(s) couldn't be saved.\n\nException: " + str(e))


    def refresh_button_clicked(self):
        self.refresh_kdms()


    def refresh_kdms(self):
        self.kdm_list.clear()
        self.clear_progress_bar()
        self.set_widgets_blocked(True)

        settings = get_settings()

        self.async_operation = Async(
            run_async=lambda progress_signal: get_kdms_from_email(settings.email_connection_settings, settings.scan_n_latest_emails, ProgressReporter(progress_signal)),
            when_done=lambda fetch_response: self.handle_kdm_response_after_fetch(fetch_response),
            progress=lambda progress: self.progressbar.setValue(progress)
        )


    def handle_kdm_response_after_fetch(self, fetchResponse: KdmFetchResponse):
        self.set_widgets_blocked(False)
        self.clear_progress_bar()

        if fetchResponse.has_response():
            self.display_kdms_in_list(fetchResponse.kdms)
        else:
            self.save_selected_button.setEnabled(False)

        if fetchResponse.is_erroneous() or fetchResponse.has_skipped_emails():
            self.launch_kdm_fetch_error_dialog(fetchResponse)


    def display_kdms_in_list(self, kdms: list[Kdm]):
        for kdm in kdms:
            item = QListWidgetItem(self.kdm_list)
            kdm_list_item = KdmListItem(kdm)
            item.setSizeHint(kdm_list_item.sizeHint())
            self.kdm_list.setItemWidget(item, kdm_list_item)


    def clear_progress_bar(self):
        self.progressbar.setValue(0)


    def set_widgets_blocked(self, blocked: bool):
        for widget in self.blockable_widgets:
            widget.setDisabled(blocked)


    def launch_settings_dialog(self, exit_app_on_close: bool = False):
        settings_dialog = SettingsDialog(exit_app_on_close)
        settings_dialog.setModal(True)
        settings_dialog.exec()


    def launch_info_dialog(self):
        info_dialog = InfoDialog()
        info_dialog.setModal(True)
        info_dialog.exec()


    def launch_error_dialog(self, title: str, description: str, initial_size: QSize = None):
        error_dialog = ErrorDialog(title, description, initial_size)
        error_dialog.setModal(True)
        error_dialog.exec()

    def launch_success_dialog(self, title: str, description: str, initial_size: QSize = None):
        error_dialog = SuccessDialog(title, description, initial_size)
        error_dialog.setModal(True)
        error_dialog.exec()

    def launch_kdm_fetch_error_dialog(self, kdm_fetch_response: KdmFetchResponse):
        error_dialog = KdmFetchErrorDialog(kdm_fetch_response)
        error_dialog.setModal(True)
        error_dialog.exec()


def launch():
    app = QApplication([])

    window = QMainWindow()
    window.setMinimumSize(400, 300)
    window.resize(900, 500)
    window.setWindowTitle("KDM-Finder")
    window.setWindowIconText("KDM-Finder")

    window.setCentralWidget(KdmFinderView())
    
    logo_pixmap = QPixmap(get_absolute_path(__file__, "..", "assets", "images", "logo.webp"))

    app.setApplicationName("KDM-Finder")
    app.setApplicationDisplayName("KDM-Finder")
    app.setWindowIcon(QIcon(logo_pixmap))

    screen_geometry = app.primaryScreen().geometry()
    center_point = screen_geometry.center()
    top_left = center_point - window.rect().center()

    window.move(top_left)

    window.show()
    app.exec()
