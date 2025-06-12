# ui/gesture_page.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

class GesturePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("手势控制")
        self.setMinimumSize(640, 480)
        self.setObjectName("ToolPage")
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        
        # 这是一个占位符，实际应用中会用 QVideoWidget 或 QLabel 显示摄像头画面
        self.camera_view = QLabel("摄像头画面区域")
        self.camera_view.setAlignment(Qt.AlignCenter)
        self.camera_view.setStyleSheet("background-color: black; color: white;")
        
        self.info_label = QLabel("手势识别已激活（实验性功能）")
        self.info_label.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(self.camera_view, stretch=1)
        layout.addWidget(self.info_label)