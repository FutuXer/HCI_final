from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QHBoxLayout

class WritingPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("写作界面")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title)

        self.text_input = QTextEdit()
        layout.addWidget(self.text_input, 5)

        button_row = QHBoxLayout()
        self.save_button = QPushButton("保存草稿")
        self.translate_button = QPushButton("翻译选中文本")
        button_row.addWidget(self.save_button)
        button_row.addWidget(self.translate_button)
        layout.addLayout(button_row)

        self.setLayout(layout)
