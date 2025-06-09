# main_ui.py
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QTextEdit, QLabel,
    QVBoxLayout, QWidget, QHBoxLayout
)
from voice import VoiceInputThread
from gesture import HandGestureThread

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI 辅助写作与翻译平台")
        self.setGeometry(100, 100, 800, 600)

        # ====== 界面组件 ======
        self.text_input = QTextEdit()
        self.text_output = QTextEdit()
        self.text_output.setReadOnly(True)

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

    def translate_text(self):
        input_text = self.text_input.toPlainText()
        if not input_text.strip():
            self.status_label.setText("状态：请输入内容后再翻译。")
            return
        # 模拟翻译输出
        translated = f"【翻译结果占位】{input_text[::-1]}"  # 假设反转为翻译效果
        self.text_output.setText(translated)
        self.status_label.setText("状态：翻译完成。")


    def ai_write(self):
        input_text = self.text_input.toPlainText()
        suggestion = f"【写作建议占位】根据内容自动生成段落: {input_text} ..."
        self.text_output.setText(suggestion)
        self.status_label.setText("状态：AI写作辅助完成。")

    def launch_gesture_module(self):
        self.status_label.setText("状态：启动手势识别线程。")
        if not self.gesture_thread:
            self.gesture_thread = HandGestureThread()
            self.gesture_thread.gesture_detected.connect(self.on_gesture_detected)
            self.gesture_thread.start()

    def on_gesture_detected(self, gesture_name):
        self.status_label.setText(f"手势识别结果：{gesture_name}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
