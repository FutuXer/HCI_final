# main_ui.py
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QTextEdit, QLabel,
    QVBoxLayout, QWidget, QHBoxLayout,
)
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QComboBox

from voice import VoiceInputThread
from gesture import HandGestureThread
from translate import baidu_translate
from ai_writer_thread import AIWriterThread  # 加到顶部


class TranslateThread(QThread):
    result_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)

    def __init__(self, text, target_lang, parent=None):
        super().__init__(parent)
        self.text = text
        self.target_lang = target_lang

    def run(self):
        try:
            result = baidu_translate(self.text, from_lang='auto', to_lang=self.target_lang)
            self.result_signal.emit(result)
        except Exception as e:
            self.error_signal.emit(str(e))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI 辅助写作与翻译平台")
        self.setGeometry(100, 100, 800, 600)

        # ====== 界面组件 ======
        self.text_input = QTextEdit()
        self.text_output = QTextEdit()
        self.text_output.setReadOnly(True)

        self.language_selector = QComboBox()
        self.language_selector.addItems([
            "中文（zh）", "英文（en）", "日文（jp）", "法语（fra）", "德语（de）", "俄语（ru）","韩语(kor)"
        ])

        self.voice_btn = QPushButton("🎤 开始语音输入")
        self.translate_btn = QPushButton("🌐 翻译文本")
        self.ai_write_btn = QPushButton("✍️ AI辅助写作")
        self.gesture_btn = QPushButton("🖐️ 启动手势识别")

        # 状态标签
        self.status_label = QLabel("状态：等待中...")

        # ====== 布局设置 ======
        layout = QVBoxLayout()
        layout.addWidget(QLabel("输入区域"))
        layout.addWidget(self.text_input)
        layout.addWidget(QLabel("目标语言："))
        layout.addWidget(self.language_selector)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.voice_btn)
        btn_layout.addWidget(self.translate_btn)
        btn_layout.addWidget(self.ai_write_btn)
        btn_layout.addWidget(self.gesture_btn)
        layout.addLayout(btn_layout)

        layout.addWidget(QLabel("输出区域"))
        layout.addWidget(self.text_output)
        layout.addWidget(self.status_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # ====== 信号绑定 ======
        self.voice_thread = None
        self.gesture_thread = None
        self.voice_btn.clicked.connect(self.toggle_voice_input)
        self.translate_btn.clicked.connect(self.translate_text)
        self.ai_write_btn.clicked.connect(self.ai_write)
        self.gesture_btn.clicked.connect(self.launch_gesture_module)

    def toggle_voice_input(self):
        if self.voice_thread and self.voice_thread.isRunning():
            self.voice_thread.stop()
            self.voice_thread = None
            self.voice_btn.setText("🎤 开始语音输入")
            self.status_label.setText("状态：语音输入已停止")
        else:
            self.voice_thread = VoiceInputThread()
            self.voice_thread.result_signal.connect(self.show_voice_result)
            self.voice_thread.start()
            self.voice_btn.setText("🛑 停止语音输入")
            self.status_label.setText("状态：正在语音识别...")

    def show_voice_result(self, text):
        self.text_input.append(f"[语音识别] {text}")

    def ai_write(self):
        input_text = self.text_input.toPlainText().strip()
        if not input_text:
            self.status_label.setText("状态：请输入内容后再进行AI写作。")
            return

        self.status_label.setText("状态：AI写作中，请稍候...")
        self.ai_writer_thread = AIWriterThread(input_text)
        self.ai_writer_thread.result_signal.connect(self.on_ai_write_result)
        self.ai_writer_thread.error_signal.connect(self.on_ai_write_error)
        self.ai_writer_thread.start()

    def on_ai_write_result(self, content):
        self.text_output.setText(content)
        self.status_label.setText("状态：AI写作完成。")

    def on_ai_write_error(self, error_msg):
        self.status_label.setText(f"状态：AI写作出错：{error_msg}")

    def launch_gesture_module(self):
        self.status_label.setText("状态：启动手势识别线程。")
        if not self.gesture_thread:
            self.gesture_thread = HandGestureThread()
            self.gesture_thread.gesture_detected.connect(self.on_gesture_detected)
            self.gesture_thread.start()

    def on_gesture_detected(self, gesture_name):
        self.status_label.setText(f"手势识别结果：{gesture_name}")

    def translate_text(self):
        input_text = self.text_input.toPlainText().strip()
        if not input_text:
            self.status_label.setText("状态：请输入内容后再翻译。")
            return
        self.status_label.setText("状态：正在翻译中，请稍候...")
        target_lang = self.get_selected_language_code()
        self.translate_thread = TranslateThread(input_text, target_lang)
        self.translate_thread.result_signal.connect(self.on_translate_result)
        self.translate_thread.error_signal.connect(self.on_translate_error)
        self.translate_thread.start()

    def on_translate_result(self, translated):
        self.text_output.setText(translated)
        self.status_label.setText("状态：翻译完成。")

    def on_translate_error(self, error_msg):
        self.status_label.setText(f"状态：翻译出错 - {error_msg}")

    def get_selected_language_code(self):
        mapping = {
            "中文（zh）": "zh",
            "英文（en）": "en",
            "日文（jp）": "jp",
            "法语（fra）": "fra",
            "德语（de）": "de",
            "俄语（ru）": "ru",
            "韩语(kor)": "kor"
        }
        return mapping.get(self.language_selector.currentText(), "zh")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
