import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from ui.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("低能AI辅助写作平台")
    app.setWindowIcon(QIcon("icons/app_icon.ico"))

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())



