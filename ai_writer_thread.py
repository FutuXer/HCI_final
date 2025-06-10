# ai_writer_thread.py
from PyQt5.QtCore import QThread, pyqtSignal
from ai_writer_api import generate_writing

class AIWriterThread(QThread):
    result_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)

    def __init__(self, prompt):
        super().__init__()
        self.prompt = prompt

    def run(self):
        try:
            result = generate_writing(self.prompt)
            self.result_signal.emit(result)
        except Exception as e:
            self.error_signal.emit(str(e))