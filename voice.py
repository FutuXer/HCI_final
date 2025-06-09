from PyQt6.QtCore import QThread, pyqtSignal
import time

class VoiceInputThread(QThread):
    result_ready = pyqtSignal(str)
    status_update = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.running = True

    def run(self):
        self.status_update.emit("🎤 正在监听语音...")
        time.sleep(2)  # 模拟语音识别延迟

        # 这里模拟识别到的语音文本
        recognized_text = "你好，这是一个语音识别示例。"
        self.status_update.emit("✅ 语音识别完成")
        self.result_ready.emit(recognized_text)

    def stop(self):
        self.running = False
        self.terminate()
        self.status_update.emit("🛑 语音识别已停止")

