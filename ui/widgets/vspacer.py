from PyQt6.QtWidgets import QSpacerItem, QSizePolicy

class VSpacer(QSpacerItem):
        def __init__(
                    self,
                    height: int = 0
            ):
            super().__init__(
                  0,
                  height,
                  QSizePolicy.Policy.Fixed,
                  QSizePolicy.Policy.MinimumExpanding if height is 0 else QSizePolicy.Policy.Fixed
            )