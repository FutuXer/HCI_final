# ui/welcome_page.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont


class WelcomePage(QWidget):
    start_new_writing = pyqtSignal()
    open_existing_file = pyqtSignal(str)
    exit_app = pyqtSignal()

    def __init__(self, parent=None):  # 👈 接收 parent 参数
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("""
            QLabel#titleLabel {
                font-size: 28px;
                font-weight: bold;
                color: #2c3e50;
            }

            QPushButton {
                font-size: 16px;
                padding: 10px;
                border-radius: 6px;
                background-color: #3498db;
                color: white;
            }

            QPushButton:hover {
                background-color: #2980b9;
            }
        """)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        self.title = QLabel("欢迎使用智能写作系统")
        self.title.setObjectName("titleLabel")
        self.title.setAlignment(Qt.AlignCenter)

        self.start_button = QPushButton("📝 开始创作")
        self.start_button.clicked.connect(self.start_new_writing.emit)

        self.open_button = QPushButton("📂 打开已有文件")
        self.open_button.clicked.connect(self.select_existing_file)

        self.exit_button = QPushButton("❌ 退出")
        self.exit_button.clicked.connect(self.exit_app.emit)

        layout.addWidget(self.title)
        layout.addSpacing(30)
        layout.addWidget(self.start_button)
        layout.addWidget(self.open_button)
        layout.addWidget(self.exit_button)

        self.setLayout(layout)

    def select_existing_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择文本文件", "", "Text Files (*.txt)")
        if file_path:
            self.open_existing_file.emit(file_path)
        else:
            QMessageBox.information(self, "提示", "没有选择文件。")