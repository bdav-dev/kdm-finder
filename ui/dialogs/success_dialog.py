from PyQt6.QtCore import QSize
from ui.dialogs.message_dialog import MessageDialog

class SuccessDialog(MessageDialog):
    
    def __init__(
            self,
            title: str,
            description: str,
            initial_size: QSize = None
        ):
        super().__init__("✓", title, description, initial_size)