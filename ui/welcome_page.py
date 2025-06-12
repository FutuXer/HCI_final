from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt

class WelcomePage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel("欢迎来到 Gesture Interactive System")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)

        start_button = QPushButton("开始写作 ✍️")
        start_button.setStyleSheet("padding: 10px; font-size: 18px;")
        start_button.clicked.connect(self.go_to_writing)
        layout.addWidget(start_button)

        self.setLayout(layout)

    def go_to_writing(self):
        self.main_window.central_stack.setCurrentIndex(1)
