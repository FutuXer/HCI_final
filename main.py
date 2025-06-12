import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from ui.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Gesture Interactive System")
    app.setWindowIcon(QIcon("icons/app_icon.ico"))

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())



