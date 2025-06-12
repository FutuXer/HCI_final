from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QWidget, QVBoxLayout, QToolBar, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize

from ui.welcome_page import WelcomePage
from ui.writing_page import WritingPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gesture Interactive System")
        self.setMinimumSize(1024, 768)

        self.central_stack = QStackedWidget()
        self.setCentralWidget(self.central_stack)

        # 页面初始化
        self.welcome_page = WelcomePage(self)
        self.writing_page = WritingPage(self)

        # 添加页面到stack
        self.central_stack.addWidget(self.welcome_page)  # index 0
        self.central_stack.addWidget(self.writing_page)  # index 1

        # 初始化菜单栏或工具栏
        self.init_toolbar()

        # 初始显示欢迎页
        self.central_stack.setCurrentIndex(0)

    def init_toolbar(self):
        toolbar = QToolBar("主菜单")
        toolbar.setIconSize(QSize(24, 24))
        self.addToolBar(toolbar)

        home_action = QAction(QIcon("icons/app_icon.ico"), "欢迎页", self)
        home_action.triggered.connect(lambda: self.central_stack.setCurrentIndex(0))
        toolbar.addAction(home_action)

        write_action = QAction(QIcon("icons/ai.png"), "写作", self)
        write_action.triggered.connect(lambda: self.central_stack.setCurrentIndex(1))
        toolbar.addAction(write_action)

        # 预留接口：可添加翻译、语音、手势等
