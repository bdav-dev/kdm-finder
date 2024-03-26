from PyQt6.QtWidgets import QWidget, QHBoxLayout
from PyQt6.QtCore import Qt

def centered(widget: QWidget):
    c = QWidget()
    c_layout = QHBoxLayout()
    c_layout.setContentsMargins(0, 0, 0, 0)

    c_layout.addWidget(widget)
    c_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    c.setLayout(c_layout)

    return c


def bottom_margin(widget: QWidget, bottom_margin: int):
    current_margins = widget.contentsMargins()

    widget.setContentsMargins(
        current_margins.left(),
        current_margins.top(),
        current_margins.right(),
        bottom_margin
    )


def top_margin(widget: QWidget, top_margin: int):
    current_margins = widget.contentsMargins()

    widget.setContentsMargins(
        current_margins.left(),
        top_margin,
        current_margins.right(),
        current_margins.bottom()
    )