# voice_page.py
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QTextEdit, QPushButton,
                             QHBoxLayout, QLabel, QApplication, QToolTip)
from PyQt5.QtCore import Qt, QSize
from ui.resources import AudioManager
from voice import VoiceInputThread


class VoiceInputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("语音输入")
        self.resize(500, 300)  # 固定初始尺寸
        self.setMinimumSize(QSize(400, 250))

        # 初始化核心组件
        self.audio = AudioManager()
        self.voice_thread = VoiceInputThread()
        self.voice_thread.moveToThread(QApplication.instance().thread())

        # 必须初始化UI后再连接信号
        self.init_ui()
        self._connect_signals()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # 状态标签（加大字体）
        self.status_label = QLabel("准备就绪")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(self.status_label)

        # 显式创建按钮属性
        self.start_btn = QPushButton("开始录音")
        self.stop_btn = QPushButton("停止录音")
        self.copy_btn = QPushButton("复制文本")
        self.clear_btn = QPushButton("清空")
        self.insert_btn = QPushButton("插入")

        # 连接信号
        self.start_btn.clicked.connect(self.start_recording)
        self.stop_btn.clicked.connect(self.stop_recording)
        self.copy_btn.clicked.connect(self.copy_text)
        self.clear_btn.clicked.connect(self.clear_text)
        self.insert_btn.clicked.connect(self.insert_to_editor)

        # 添加到布局
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.start_btn)
        btn_layout.addWidget(self.stop_btn)
        btn_layout.addWidget(self.copy_btn)
        btn_layout.addWidget(self.clear_btn)
        btn_layout.addWidget(self.insert_btn)

        self.stop_btn.setEnabled(False)  # 现在可以安全访问
        layout.addLayout(btn_layout)

        # 文本显示区（最小高度设置）
        self.text_edit = QTextEdit()
        self.text_edit.setMinimumHeight(150)
        self.text_edit.setPlaceholderText("语音识别结果将显示在这里...")
        layout.addWidget(self.text_edit)

        self.stop_btn.setEnabled(False)
        layout.addLayout(btn_layout)

    def _connect_signals(self):
        """集中管理信号槽连接"""
        self.voice_thread.result_ready.connect(self.append_voice_text)
        self.voice_thread.status_update.connect(self.update_status)
        self.voice_thread.error_occurred.connect(self.show_error)

        if hasattr(self.audio, 'error_signal'):
            self.audio.error_signal.connect(self.show_error)

    def start_recording(self):
        try:
            print("尝试启动录音...")  # 调试输出
            self.start_btn.setEnabled(False)
            self.stop_btn.setEnabled(True)
            if not self.voice_thread.isRunning():
                print("启动语音输入线程...")
                self.voice_thread.start()
                print("线程启动成功")
        except Exception as e:
            error_msg = f"启动失败: {str(e)}"
            print(error_msg)  # 控制台输出详细错误
            self.show_error(error_msg)
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)

    def stop_recording(self):
        self.voice_thread.stop()
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)

    def append_voice_text(self, text):
        current_text = self.text_edit.toPlainText()
        if current_text:
            # Add space between existing text and new text
            new_text = f"{current_text} {text}"
        else:
            new_text = text
        self.text_edit.setPlainText(new_text)

    def update_status(self, message):
        self.status_label.setText(message)

    def show_error(self, error_msg):
        self.status_label.setText(error_msg)
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)

    def copy_text(self):
        text = self.text_edit.toPlainText()
        if text:
            clipboard = QApplication.clipboard()
            clipboard.setText(text)
            QToolTip.showText(self.copy_btn.mapToGlobal(self.copy_btn.rect().center()),
                              "复制成功 ✅", self.copy_btn)

    def clear_text(self):
        self.text_edit.clear()

    def insert_to_editor(self):
        text = self.text_edit.toPlainText()
        if text and self.parent():
            self.parent().text_edit.insertPlainText(text)
            self.close()

    def closeEvent(self, event):
        self.voice_thread.stop()
        super().closeEvent(event)