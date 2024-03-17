from PyQt6.QtWidgets import QFrame


class Hr(QFrame):
    
    def __init__(self):
        super(Hr, self).__init__()

        self.setFrameShape(QFrame.Shape.HLine)
        self.setFrameShadow(QFrame.Shadow.Sunken)