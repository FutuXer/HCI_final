# ui/welcome_page.py (完整替换)

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QCursor

class WelcomePage(QWidget):
    """
    功能更完善的欢迎页。
    在主操作外，提供次要操作入口。
    """
    start_creation = pyqtSignal()
    open_txt_file = pyqtSignal()  # --- 新增信号 ---
    exit_app = pyqtSignal()       # --- 新增信号 ---

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("WelcomePage")
        self.init_ui()

    def init_ui(self):
        """初始化UI元素和布局。"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(50, 50, 50, 50)
        main_layout.setSpacing(0)
        main_layout.setAlignment(Qt.AlignCenter)

        main_layout.addStretch()

        title = QLabel("欢迎使用\n交互式写作平台")
        title.setObjectName("WelcomeTitle")
        title.setAlignment(Qt.AlignCenter)
        title.setWordWrap(True)

        subtitle = QLabel("一个为创作者设计的现代AI辅助工具")
        subtitle.setObjectName("WelcomeSubtitle")
        subtitle.setAlignment(Qt.AlignCenter)

        enter_btn = QPushButton("🚀  进入工作区")
        enter_btn.setObjectName("WelcomeButton")
        enter_btn.setCursor(QCursor(Qt.PointingHandCursor))
        enter_btn.clicked.connect(self.start_creation.emit)
        
        # --- 新增：次要操作按钮 ---
        secondary_actions_layout = QHBoxLayout()
        secondary_actions_layout.setSpacing(20)

        open_btn = QPushButton("📂 打开文件")
        open_btn.setObjectName("SecondaryWelcomeButton")
        open_btn.setCursor(QCursor(Qt.PointingHandCursor))
        open_btn.clicked.connect(self.open_txt_file.emit)

        exit_btn = QPushButton("❌ 退出")
        exit_btn.setObjectName("SecondaryWelcomeButton")
        exit_btn.setCursor(QCursor(Qt.PointingHandCursor))
        exit_btn.clicked.connect(self.exit_app.emit)

        secondary_actions_layout.addWidget(open_btn)
        secondary_actions_layout.addWidget(exit_btn)
        # --- 新增结束 ---

        main_layout.addWidget(title)
        main_layout.addSpacing(20)
        main_layout.addWidget(subtitle)
        main_layout.addSpacing(60)
        main_layout.addWidget(enter_btn, alignment=Qt.AlignCenter)
        main_layout.addSpacing(25) # 在主按钮和次要按钮间增加间距
        main_layout.addLayout(secondary_actions_layout) # 添加次要按钮布局

        main_layout.addStretch()