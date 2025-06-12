# ui/writing_page.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QFileDialog, QMessageBox, QHBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
import os


class WritingPage(QWidget):
    back_to_welcome = pyqtSignal()
    save_file = pyqtSignal(str, str)  # (filepath, content)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_file_path = None
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("""
            QLabel#titleLabel {
                font-size: 22px;
                font-weight: bold;
                color: #34495e;
            }

            QPushButton {
                font-size: 14px;
                padding: 6px 12px;
                border-radius: 5px;
                background-color: #27ae60;
                color: white;
            }

            QPushButton:hover {
                background-color: #219150;
            }

            QTextEdit {
                font-size: 14px;
                padding: 10px;
            }
        """)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)

        # 顶部标题和按钮栏
        top_bar = QHBoxLayout()
        self.title_label = QLabel("新建写作项目")
        self.title_label.setObjectName("titleLabel")

        self.save_btn = QPushButton("保存")
        self.save_btn.clicked.connect(self.save_content)

        self.back_btn = QPushButton("返回欢迎页")
        self.back_btn.clicked.connect(lambda: self.back_to_welcome.emit())

        top_bar.addWidget(self.title_label)
        top_bar.addStretch()
        top_bar.addWidget(self.save_btn)
        top_bar.addWidget(self.back_btn)

        main_layout.addLayout(top_bar)

        # 主要文本编辑区
        self.text_edit = QTextEdit()
        main_layout.addWidget(self.text_edit, stretch=1)

        self.setLayout(main_layout)

    def load_file(self, file_path):
        """加载已有文件内容"""
        if file_path and os.path.isfile(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                self.text_edit.setPlainText(content)
                self.current_file_path = file_path
                self.title_label.setText(f"编辑文件: {os.path.basename(file_path)}")
            except Exception as e:
                QMessageBox.warning(self, "加载失败", f"无法读取文件:\n{str(e)}")
        else:
            self.current_file_path = None
            self.title_label.setText("新建写作项目")
            self.text_edit.clear()

    def save_content(self):
        content = self.text_edit.toPlainText()
        if self.current_file_path:
            try:
                with open(self.current_file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                QMessageBox.information(self, "保存成功", f"已保存文件：{self.current_file_path}")
            except Exception as e:
                QMessageBox.warning(self, "保存失败", f"无法保存文件:\n{str(e)}")
        else:
            # 没有打开文件，弹出保存对话框
            file_path, _ = QFileDialog.getSaveFileName(self, "保存文件", "", "文本文件 (*.txt)")
            if file_path:
                try:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(content)
                    self.current_file_path = file_path
                    self.title_label.setText(f"编辑文件: {os.path.basename(file_path)}")
                    QMessageBox.information(self, "保存成功", f"已保存文件：{file_path}")
                except Exception as e:
                    QMessageBox.warning(self, "保存失败", f"无法保存文件:\n{str(e)}")
            else:
                QMessageBox.information(self, "保存取消", "文件未保存。")
