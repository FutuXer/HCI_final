# ui/resources.py
from PyQt5.QtCore import QObject, pyqtSignal
import pyaudio


class AudioManager(QObject):
    _instance = None
    error_signal = pyqtSignal(str)

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            try:
                cls._instance.p = pyaudio.PyAudio()
            except Exception as e:
                cls._instance.error_signal.emit(f"音频初始化失败: {str(e)}")
                raise
        return cls._instance

    def get_stream(self, callback):
        try:
            return self.p.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=1024,
                stream_callback=callback
            )
        except Exception as e:
            self.error_signal.emit(f"无法打开音频流: {str(e)}")
            return None