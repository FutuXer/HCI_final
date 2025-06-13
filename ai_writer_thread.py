# ai_writer_thread.py
from PyQt5.QtCore import QThread, pyqtSignal

class AIWriterThread(QThread):
    result_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)

    def __init__(self, mode, prompt):
        super().__init__()
        self.prompt = prompt
        self.mode = mode

    def run(self):
        print(f"[AIWriterThread] 启动线程，模式：{self.mode}，内容：{self.prompt}")
        try:
            from ai_writer_api import generate_writing
            result = generate_writing(self.mode, self.prompt)
            self.result_signal.emit(result)
        except Exception as e:
            self.error_signal.emit(str(e))
