from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton, QHBoxLayout, QApplication, QToolTip
class AIResultDialog(QDialog):
    def __init__(self, result_text, parent=None):
        super().__init__(parent)
        self.setWindowTitle("AI 写作结果")
        self.resize(600, 400)

        layout = QVBoxLayout(self)

        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        self.text_edit.setPlainText(result_text)
        layout.addWidget(self.text_edit)

        btn_layout = QHBoxLayout()
        self.copy_btn = QPushButton("复制文本", self)
        self.copy_btn.clicked.connect(self.copy_text)
        self.close_btn = QPushButton("关闭", self)
        self.close_btn.clicked.connect(self.accept)
        btn_layout.addWidget(self.copy_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(self.close_btn)

        layout.addLayout(btn_layout)

    def copy_text(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.text_edit.toPlainText())

    def copy_text(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.text_edit.toPlainText())
        QToolTip.showText(self.copy_btn.mapToGlobal(self.copy_btn.rect().center()), "复制成功 ✅", self.copy_btn)