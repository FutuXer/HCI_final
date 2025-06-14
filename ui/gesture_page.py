# gesture_page.py
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLabel, QPushButton,
                             QHBoxLayout, QTextEdit, QApplication)
from PyQt5.QtCore import Qt, pyqtSignal
from gesture import HandGestureThread
import time


class GestureControlDialog(QDialog):
    gesture_detected = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("手势控制")
        self.resize(400, 300)

        self.gesture_thread = HandGestureThread()
        self.gesture_thread.gesture_detected.connect(self.handle_gesture)

        self.init_ui()

        self.last_gesture = None
        self.last_gesture_time = 0
        self.gesture_cooldown = 2  # 2秒冷却，防止连续触发

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Instruction label
        instruction = QLabel("手势控制说明：\n"
                             "👆 食指 - 插入光标位置\n"
                             "✌️ 剪刀手 - 复制选中文本\n"
                             "✊ 拳头 - 粘贴文本\n"
                             "🖐️ 张开手掌 - 保存文档\n"
                             "🤘 摇滚手势 - 返回欢迎页")
        instruction.setAlignment(Qt.AlignCenter)
        layout.addWidget(instruction)

        # Gesture display
        self.gesture_label = QLabel("等待检测手势...")
        self.gesture_label.setAlignment(Qt.AlignCenter)
        self.gesture_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(self.gesture_label)

        # Log display
        self.log_edit = QTextEdit()
        self.log_edit.setReadOnly(True)
        self.log_edit.setMaximumHeight(100)
        layout.addWidget(self.log_edit)

        # Button layout
        btn_layout = QHBoxLayout()

        self.start_btn = QPushButton("开始检测", self)
        self.start_btn.clicked.connect(self.start_detection)
        btn_layout.addWidget(self.start_btn)

        self.stop_btn = QPushButton("停止检测", self)
        self.stop_btn.clicked.connect(self.stop_detection)
        self.stop_btn.setEnabled(False)
        btn_layout.addWidget(self.stop_btn)

        self.close_btn = QPushButton("关闭", self)
        self.close_btn.clicked.connect(self.close)
        btn_layout.addWidget(self.close_btn)

        layout.addLayout(btn_layout)

    def start_detection(self):
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.gesture_thread.start()
        self.log_message("手势检测已启动")

    def stop_detection(self):
        self.gesture_thread.stop()
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.log_message("手势检测已停止")

    def handle_gesture(self, gesture):
        now = time.time()

        # 手势变化或冷却时间到，才处理
        if gesture != self.last_gesture or (now - self.last_gesture_time) > self.gesture_cooldown:
            self.last_gesture = gesture
            self.last_gesture_time = now

            self.gesture_label.setText(gesture)

            if not self.parent():
                return

            text_edit = self.parent().text_edit
            cursor = text_edit.textCursor()

            if gesture == "Index Finger":
                self.log_message("食指手势: 准备输入")

            elif gesture == "Scissor":
                if cursor.hasSelection():
                    clipboard = QApplication.clipboard()
                    clipboard.setText(cursor.selectedText())
                    self.log_message("剪刀手势: 已复制选中文本")

            elif gesture == "Fist":
                clipboard = QApplication.clipboard()
                text_edit.insertPlainText(clipboard.text())
                self.log_message("拳头手势: 已粘贴文本")

            elif gesture == "Open Palm":
                self.parent().save_content()
                self.log_message("张开手掌: 已保存文档")

            elif gesture == "Rock Gesture":
                self.parent().back_to_welcome.emit()
                self.log_message("摇滚手势: 返回欢迎页")
        else:
            # 冷却期内忽略重复手势
            pass

    def log_message(self, message):
        self.log_edit.append(message)

    def closeEvent(self, event):
        self.stop_detection()
        super().closeEvent(event)