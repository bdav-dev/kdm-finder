from PyQt6.QtWidgets import QSpacerItem, QSizePolicy

class HSpacer(QSpacerItem):
        def __init__(
                    self,
                    width: int = 0
            ):
            super().__init__(
                  width,
                  0,
                  QSizePolicy.Policy.MinimumExpanding if width is 0 else QSizePolicy.Policy.Fixed,
                  QSizePolicy.Policy.Fixed
            )