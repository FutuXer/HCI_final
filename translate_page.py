# ui/translate_page.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

class TranslatePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        label = QLabel("这里是翻译功能页面\n(UI待实现)")
        label.setAlignment(Qt.AlignCenter)
        label.setObjectName("PagePlaceholderLabel")
        layout.addWidget(label)