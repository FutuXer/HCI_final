# main.py

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from ui.main_window import MainWindow

if __name__ == '__main__':
    # --- 核心修正 ---
    # 必须在创建 QApplication 实例之前设置这些属性
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    
    # 现在才创建 QApplication 实例
    app = QApplication(sys.argv)
    
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())