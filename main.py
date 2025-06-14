import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from ui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)

    # 预初始化音频系统
    from ui.resources import AudioManager
    AudioManager()  # 提前实例化

    from ui.main_window import MainWindow
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("AI辅助写作平台")
    app.setWindowIcon(QIcon("icons/app_icon.ico"))


    window = MainWindow()
    window.show()

    sys.exit(app.exec_())