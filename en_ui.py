from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QLabel, QTextEdit,
    QVBoxLayout, QHBoxLayout, QStackedWidget, QListWidget, QSplitter,
    QFrame, QComboBox, QToolBar, QAction, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import sys


class WelcomePage(QWidget):
    def __init__(self, switch_callback):
        super().__init__()
        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(QLabel("<h1>欢迎使用智能交互平台</h1>"), alignment=Qt.AlignCenter)

        self.write_button = QPushButton("📝 开始写作")
        self.translate_button = QPushButton("🌐 翻译助手")
        self.voice_button = QPushButton("🎤 语音交互")
        self.gesture_button = QPushButton("✋ 手势识别")

        for btn in [self.write_button, self.translate_button, self.voice_button, self.gesture_button]:
            btn.setMinimumHeight(50)
            layout.addWidget(btn, alignment=Qt.AlignCenter)

        layout.addStretch()
        self.setLayout(layout)

        self.write_button.clicked.connect(lambda: switch_callback("write"))
        self.translate_button.clicked.connect(lambda: switch_callback("translate"))
        self.voice_button.clicked.connect(lambda: switch_callback("voice"))
        self.gesture_button.clicked.connect(lambda: switch_callback("gesture"))


class WritingPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("<h2>写作界面</h2>"))
        layout.addWidget(QTextEdit("在这里撰写内容..."))
        self.setLayout(layout)


class TranslationPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("<h2>翻译助手</h2>"))
        layout.addWidget(QTextEdit("输入待翻译内容..."))
        lang_select = QComboBox()
        lang_select.addItems(["中文", "英文", "日文", "法文"])
        layout.addWidget(lang_select)
        layout.addWidget(QTextEdit("翻译结果显示在这里..."))
        self.setLayout(layout)


class VoicePage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("<h2>语音输入模块</h2>"))
        layout.addWidget(QTextEdit("语音转文本将在此显示..."))
        self.setLayout(layout)


class GesturePage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("<h2>手势识别模块</h2>"))
        layout.addWidget(QLabel("此处将显示手势输入结果..."))
        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("智能交互系统")
        self.setGeometry(100, 100, 1000, 700)
        self.setWindowIcon(QIcon("icons/app_icon.ico"))

        self.stack = QStackedWidget()
        self.pages = {
            "welcome": WelcomePage(self.switch_page),
            "write": WritingPage(),
            "translate": TranslationPage(),
            "voice": VoicePage(),
            "gesture": GesturePage()
        }

        for page in self.pages.values():
            self.stack.addWidget(page)

        self.setCentralWidget(self.stack)
        self.switch_page("welcome")
        self._create_toolbar()

    def _create_toolbar(self):
        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)
        self.addToolBar(Qt.TopToolBarArea, toolbar)

        home_action = QAction("🏠 首页", self)
        home_action.triggered.connect(lambda: self.switch_page("welcome"))
        toolbar.addAction(home_action)

        write_action = QAction("📝 写作", self)
        write_action.triggered.connect(lambda: self.switch_page("write"))
        toolbar.addAction(write_action)

        translate_action = QAction("🌐 翻译", self)
        translate_action.triggered.connect(lambda: self.switch_page("translate"))
        toolbar.addAction(translate_action)

        voice_action = QAction("🎤 语音", self)
        voice_action.triggered.connect(lambda: self.switch_page("voice"))
        toolbar.addAction(voice_action)

        gesture_action = QAction("✋ 手势", self)
        gesture_action.triggered.connect(lambda: self.switch_page("gesture"))
        toolbar.addAction(gesture_action)

    def switch_page(self, name):
        self.stack.setCurrentWidget(self.pages[name])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
