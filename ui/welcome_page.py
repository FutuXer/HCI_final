from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy
from PyQt5.QtCore import pyqtSignal, Qt


class WelcomePage(QWidget):
    start_creation = pyqtSignal()
    open_txt_file = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        # 设置整体布局
        layout = QVBoxLayout()
        layout.setContentsMargins(60, 60, 60, 60)
        layout.setSpacing(30)
        layout.setAlignment(Qt.AlignCenter)

        # 标题
        title = QLabel("欢迎使用交互式写作平台")
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #333;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Spacer让按钮整体垂直居中
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # 按钮样式统一定义
        button_style = """
            QPushButton {
                font-size: 18px;
                padding: 12px 24px;
                border: 2px solid #555;
                border-radius: 8px;
                background-color: #f0f0f0;
            }
            QPushButton:hover {
                background-color: #d0e8ff;
            }
        """

        # 开始创作按钮
        create_btn = QPushButton("📝 开始创作")
        create_btn.setStyleSheet(button_style)
        create_btn.clicked.connect(self.start_creation.emit)
        layout.addWidget(create_btn, alignment=Qt.AlignCenter)

        # 打开文件按钮
        open_btn = QPushButton("📂 打开本地 TXT 文件")
        open_btn.setStyleSheet(button_style)
        open_btn.clicked.connect(self.open_txt_file.emit)
        layout.addWidget(open_btn, alignment=Qt.AlignCenter)

        # 退出按钮
        exit_btn = QPushButton("❌ 退出程序")
        exit_btn.setStyleSheet(button_style)
        exit_btn.clicked.connect(self.close_app)
        layout.addWidget(exit_btn, alignment=Qt.AlignCenter)

        # Spacer 底部
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(layout)

    def close_app(self):
        from PyQt5.QtWidgets import QApplication
        QApplication.quit()
