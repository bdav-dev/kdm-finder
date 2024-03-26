from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QPushButton
from PyQt6.QtCore import Qt


class PasswordLineEdit(QWidget):
    
    def __init__(self):
        super().__init__()

        self.is_password_hidden = True

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.password_line_edit = QLineEdit()

        self.pw_show_hide_button = QPushButton()
        self.pw_show_hide_button.setFixedWidth(50)
        self.pw_show_hide_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.pw_show_hide_button.clicked.connect(self.toggle_password_hidden)
        
        layout.addWidget(self.password_line_edit)
        layout.addWidget(self.pw_show_hide_button)

        self.setLayout(layout)

        self.set_password_hidden(True)


    def set_password_hidden(self, hidden):
        self.is_password_hidden = hidden

        if hidden:
            self.pw_show_hide_button.setText("Show")
            self.password_line_edit.setEchoMode(QLineEdit.EchoMode.Password)
        else:
            self.pw_show_hide_button.setText("Hide")
            self.password_line_edit.setEchoMode(QLineEdit.EchoMode.Normal)


    def toggle_password_hidden(self):
        self.set_password_hidden(not self.is_password_hidden)


    def get_password(self) -> str:
        return self.password_line_edit.text()
    

    def set_password(self, password: str):
        self.password_line_edit.setText(password)
