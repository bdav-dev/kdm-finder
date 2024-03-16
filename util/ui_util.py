from PyQt6.QtWidgets import QWidget, QHBoxLayout
from PyQt6.QtCore import Qt

def centered(widget):
    c = QWidget()
    c_layout = QHBoxLayout()
    c_layout.setContentsMargins(0, 0, 0, 0)

    c_layout.addWidget(widget)
    c_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    c.setLayout(c_layout)

    return c
