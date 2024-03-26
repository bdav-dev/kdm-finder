from typing import Callable
from PyQt6.QtCore import QThread, pyqtSignal

class Async(QThread):
    finished_signal = pyqtSignal(object)
    progress_signal = pyqtSignal(int)

    def __init__(
            self,
            run_async: Callable[[any], any],
            when_done: Callable[[any], None],
            progress: Callable[[int], None]
        ):
        super().__init__()
        self.run_async = run_async
        self.finished_signal.connect(when_done)
        self.progress_signal.connect(progress)

        self.start()

    def run(self):
        result = self.run_async(self.progress_signal)
        self.finished_signal.emit(result)