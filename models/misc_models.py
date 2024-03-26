
class ProgressReporter:

    def __init__(
            self,
            progress_signal
        ):
        self.value: int = 0
        self.max_value: int = 100
        self.progress_signal = progress_signal


    def next(self):
        self.value = self.value + 1
        self._report_progress()


    def _report_progress(self):
        value_from_0_to_100 = (self.value / self.max_value) * 100
        self.progress_signal.emit(int(value_from_0_to_100))


    def clear(self):
        self.progress_signal.emit(0)
