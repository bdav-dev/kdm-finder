from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel,  QSizePolicy, QPushButton
from PyQt6.QtCore import Qt
from ui.widgets.hr import Hr
from ui.widgets.vspacer import VSpacer
from util.ui_util import centered

class ErrorDialog(QDialog):
    def __init__(
            self,
            title: str,
            description: str
        ):
        super().__init__()

        self.setMaximumSize(700, 400)
        self.setMinimumSize(310, 210)
        self.setWindowTitle(title)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        exclamation_mark_label = QLabel("!")
        exclamation_mark_label.setStyleSheet("font-size: 35pt;")

        title_label = QLabel(title)
        title_label.setWordWrap(True)
        
        description_label = QLabel(description)
        description_label.setWordWrap(True)
        description_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        description_label.setAlignment(Qt.AlignmentFlag.AlignTop)

        ok_button = QPushButton("Ok")
        ok_button.clicked.connect(self.close)

        layout.addWidget(centered(exclamation_mark_label))
        layout.addWidget(centered(title_label))
        layout.addItem(VSpacer(10))
        layout.addWidget(Hr())
        layout.addItem(VSpacer(10))
        layout.addWidget(centered(description_label))
        layout.addItem(VSpacer(10))
        layout.addWidget(Hr())
        layout.addItem(VSpacer(5))
        layout.addWidget(ok_button)

        self.setLayout(layout)