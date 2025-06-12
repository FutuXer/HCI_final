# ui/main_window.py

from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt
from ui.welcome_page import WelcomePage
from ui.writing_page import WritingPage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("低能写作平台")
        self.resize(900, 600)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # 初始化两个页面
        self.welcome_page = WelcomePage()
        self.writing_page = WritingPage()

        # 添加到堆栈控件
        self.stacked_widget.addWidget(self.welcome_page)   # index 0
        self.stacked_widget.addWidget(self.writing_page)   # index 1

        # 默认显示欢迎页
        self.stacked_widget.setCurrentIndex(0)

        # 信号连接
        self.welcome_page.start_creation.connect(self.show_writing_page_new)
        self.welcome_page.open_txt_file.connect(self.show_writing_page_open)

        self.writing_page.back_to_welcome.connect(self.show_welcome_page)

    def show_welcome_page(self):
        self.stacked_widget.setCurrentIndex(0)
        # 清理写作页内容（选项）
        self.writing_page.text_edit.clear()
        self.writing_page.current_file_path = None
        self.writing_page.title_label.setText("新建写作项目")

    def show_writing_page_new(self):
        self.stacked_widget.setCurrentIndex(1)
        self.writing_page.load_file(None)  # 新建写作，不加载文件

    def show_writing_page_open(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "打开文本文件", "", "文本文件 (*.txt)")
        if file_path:
            self.stacked_widget.setCurrentIndex(1)
            self.writing_page.load_file(file_path)
        else:
            QMessageBox.information(self, "打开取消", "没有选择任何文件。")

