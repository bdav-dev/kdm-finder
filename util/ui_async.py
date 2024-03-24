from typing import Callable
from PyQt6.QtCore import QThread, pyqtSignal



class Async(QThread):
    finished = pyqtSignal(object)

    def __init__(
            self,
            run_async: Callable[[], any],
            when_done: Callable[[any], None]
        ):
        super().__init__()
        self.run_async = run_async
        self.finished.connect(when_done)
        self.start()

    def run(self):
        result = self.run_async()
        self.finished.emit(result)