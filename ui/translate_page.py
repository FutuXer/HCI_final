from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton,
    QHBoxLayout, QComboBox, QMessageBox, QSpacerItem, QSizePolicy, QApplication
)
from PyQt5.QtCore import Qt
import translate

class TranslatePage(QWidget):
    def __init__(self, get_main_text_callback=None):
        super().__init__()

        self.get_main_text_callback = get_main_text_callback  # 外部传入获取主界面内容的函数

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

            QComboBox {
                font-size: 14px;
                padding: 4px 10px;
                border: 2px solid #27ae60;
                border-radius: 8px;
                color: #27ae60;
                background-color: white;
                min-width: 120px;
            }

            QComboBox::drop-down {
                border: none;
            }

            QComboBox QAbstractItemView {
                border: 1px solid #27ae60;
                selection-background-color: #27ae60;
                color: black;
            }
        """)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # 原文显示框
        self.original_text = QTextEdit()
        self.original_text.setPlaceholderText("请输入或粘贴要翻译的内容...")
        layout.addWidget(QLabel("原文内容："))
        layout.addWidget(self.original_text)

        self.copy_main_btn = QPushButton("从主界面复制")
        self.copy_main_btn.clicked.connect(self.copy_from_main)
        layout.addWidget(self.copy_main_btn)

        # 语言选择 + 翻译按钮 + 复制主界面内容按钮
        control_layout = QHBoxLayout()

        control_layout.addWidget(QLabel("目标语言："))
        self.language_selector = QComboBox()
        self.language_selector.addItems([
            "中文 (zh)", "英文 (en)", "日文 (jp)", "韩文 (kor)", "法文 (fra)", "德文 (de)"
        ])
        control_layout.addWidget(self.language_selector)

        self.translate_btn = QPushButton("翻译")
        self.translate_btn.clicked.connect(self.translate_text)
        control_layout.addWidget(self.translate_btn)


        control_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        layout.addLayout(control_layout)

        # 翻译结果框
        layout.addWidget(QLabel("翻译结果："))
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        layout.addWidget(self.result_text)

        # 复制按钮
        self.copy_btn = QPushButton("复制翻译结果")
        self.copy_btn.clicked.connect(self.copy_result)
        layout.addWidget(self.copy_btn, alignment=Qt.AlignRight)

        self.setLayout(layout)

    def translate_text(self):
        source_text = self.original_text.toPlainText().strip()
        if not source_text:
            QMessageBox.information(self, "提示", "请输入要翻译的内容")
            return

        lang_code = self.language_selector.currentText().split("(")[-1].strip(")")
        try:
            translated = translate.baidu_translate(source_text, to_lang=lang_code)
            self.result_text.setPlainText(translated)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"翻译失败：{str(e)}")

    def copy_result(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.result_text.toPlainText())
        QMessageBox.information(self, "复制成功", "翻译结果已复制到剪贴板")

    def copy_from_main(self):
        if self.get_main_text_callback:
            main_text = self.get_main_text_callback()
            if main_text:
                self.original_text.setPlainText(main_text)
                QMessageBox.information(self, "复制成功", "已从主界面复制内容到原文框")
            else:
                QMessageBox.warning(self, "提示", "主界面内容为空")
        else:
            QMessageBox.warning(self, "错误", "未设置获取主界面内容的回调函数")
