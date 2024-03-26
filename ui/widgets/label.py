
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt


class Label(QWidget):

    def __init__(
            self,
            widget: QWidget,
            label_text: str,
            label_width: int = None
        ):
        super().__init__()

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.widget = widget

        self.label = QLabel(label_text)
        self.label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        layout.addWidget(self.label)
        layout.addWidget(widget)

        self.setLayout(layout)

        if label_width is not None:
            self.set_label_width(label_width)


    def set_label_width(self, width):
        self.label.setFixedWidth(width)


