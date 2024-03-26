from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QTextEdit
from PyQt6.QtCore import Qt, QSize
from ui.widgets.hr import Hr
from ui.widgets.vspacer import VSpacer
from util.ui_util import centered

class ErrorDialog(QDialog):
    
    def __init__(
            self,
            title: str,
            description: str,
            initial_size: QSize = None
        ):
        super().__init__()

        self.setMaximumSize(900, 600)
        self.setMinimumSize(310, 210)
        self.setWindowTitle(title)

        if initial_size == None:
            initial_size = QSize(440, 330)

        self.resize(initial_size.width(), initial_size.height())

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        exclamation_mark_label = QLabel("!")
        exclamation_mark_label.setStyleSheet("font-size: 35pt;")

        title_label = QLabel(title)
        title_label.setWordWrap(True)
        
        description_textedit = QTextEdit()
        description_textedit.setReadOnly(True)
        description_textedit.setText(description)

        ok_button = QPushButton("Ok")
        ok_button.clicked.connect(self.close)

        layout.addWidget(centered(exclamation_mark_label))
        layout.addWidget(centered(title_label))
        layout.addItem(VSpacer(10))
        layout.addWidget(Hr())
        layout.addItem(VSpacer(10))
        layout.addWidget(description_textedit)
        layout.addItem(VSpacer(10))
        layout.addWidget(Hr())
        layout.addItem(VSpacer(5))
        layout.addWidget(ok_button)

        self.setLayout(layout)