from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QFileDialog,
    QMessageBox, QHBoxLayout, QToolBar, QAction, QSizePolicy, QSpacerItem,
    QListWidget, QListWidgetItem, QSplitter, QDialog,
)
from PyQt5.QtGui import QFont, QIcon, QTextCursor, QTextDocument, QMovie
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtWidgets import QMessageBox

from ai_writer_thread import AIWriterThread
from ui.ai_page import AIResultDialog

import os
import re

class WritingPage(QWidget):
    back_to_welcome = pyqtSignal()
    save_file = pyqtSignal(str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_file_path = None
        self.heading_positions = []
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
        main_layout.setSpacing(10)

        # 顶部标题和按钮栏
        top_bar = QHBoxLayout()
        self.title_label = QLabel("新建写作项目")
        self.title_label.setObjectName("titleLabel")

        self.toggle_toc_btn = QPushButton("收起目录栏")
        self.toggle_toc_btn.clicked.connect(self.toggle_toc)

        self.save_btn = QPushButton("保存")
        self.save_btn.clicked.connect(self.save_content)

        self.back_btn = QPushButton("返回欢迎页")
        self.back_btn.clicked.connect(lambda: self.back_to_welcome.emit())

        top_bar.addWidget(self.title_label)
        top_bar.addStretch()
        top_bar.addWidget(self.toggle_toc_btn)
        top_bar.addWidget(self.save_btn)
        top_bar.addWidget(self.back_btn)
        main_layout.addLayout(top_bar)

        # 中部区域：目录栏 + 文本编辑
        self.splitter = QSplitter(Qt.Horizontal)

        self.toc_list = QListWidget()
        self.toc_list.setMaximumWidth(220)
        self.toc_list.setStyleSheet("font-size: 13px;")
        self.toc_list.itemClicked.connect(self.scroll_to_heading)

        self.text_edit = QTextEdit()
        self.text_edit.textChanged.connect(self.update_word_count)

        self.splitter.addWidget(self.toc_list)
        self.splitter.addWidget(self.text_edit)
        self.splitter.setStretchFactor(1, 1)

        # 工具栏
        toolbar = QToolBar("编辑工具栏")
        toolbar.setIconSize(QSize(25, 25))

        undo_action = QAction(QIcon("icons/undo.png"), "撤销", self)
        undo_action.triggered.connect(self.undo_text)
        toolbar.addAction(undo_action)

        redo_action = QAction(QIcon("icons/redo.png"), "重做", self)
        redo_action.triggered.connect(self.redo_text)
        toolbar.addAction(redo_action)

        docx_action = QAction(QIcon("icons/save_docx.png"), "保存为 DOCX", self)
        docx_action.triggered.connect(self.save_as_docx)
        toolbar.addAction(docx_action)

        txt_action = QAction(QIcon("icons/txt.png"), "保存为 TXT", self)
        txt_action.triggered.connect(self.save_as_txt)
        toolbar.addAction(txt_action)

        pdf_action = QAction(QIcon("icons/pdf.png"), "导出为 PDF", self)
        pdf_action.triggered.connect(self.export_as_pdf)
        toolbar.addAction(pdf_action)

        html_action = QAction(QIcon("icons/html.png"), "导出为 HTML", self)
        html_action.triggered.connect(self.save_as_html)
        toolbar.addAction(html_action)

        insert_line_action = QAction(QIcon("icons/divide.png"), "插入分割线", self)
        insert_line_action.triggered.connect(self.insert_divider)
        toolbar.addAction(insert_line_action)

        insert_paragraph_action = QAction(QIcon("icons/para.png"), "插入段落", self)
        insert_paragraph_action.triggered.connect(self.insert_paragraph)
        toolbar.addAction(insert_paragraph_action)

        zoom_in_action = QAction(QIcon("icons/zoom_in.png"), "放大字体", self)
        zoom_in_action.triggered.connect(lambda: self.text_edit.zoomIn(1))
        toolbar.addAction(zoom_in_action)

        zoom_out_action = QAction(QIcon("icons/zoom_out.png"), "缩小字体", self)
        zoom_out_action.triggered.connect(lambda: self.text_edit.zoomOut(1))
        toolbar.addAction(zoom_out_action)

        # AI扩写按钮
        expand_action = QAction(QIcon("icons/expand.png"), "AI 扩写", self)
        expand_action.triggered.connect(lambda: self.call_ai_writer("扩写"))
        toolbar.addAction(expand_action)

        polish_action = QAction(QIcon("icons/polish.png"), "AI 润色", self)
        polish_action.triggered.connect(lambda: self.call_ai_writer("润色"))
        toolbar.addAction(polish_action)

        main_layout.addWidget(toolbar)
        main_layout.addWidget(self.splitter, stretch=1)  # 给splitter一个拉伸因子1

        # 沙漏动画初始化
        self.loading_label = QLabel(self)
        self.loading_movie = QMovie("icons/busy.gif")
        self.loading_label.setMovie(self.loading_movie)
        self.loading_label.setFixedSize(64, 64)
        self.loading_label.setScaledContents(True)
        self.loading_label.hide()

        # 字数统计
        self.word_count_label = QLabel("字数：0")
        self.word_count_label.setAlignment(Qt.AlignRight)
        main_layout.addWidget(self.word_count_label)

        self.setLayout(main_layout)

    def toggle_toc(self):
        if self.toc_list.isVisible():
            self.toc_list.hide()
            self.toggle_toc_btn.setText("展开目录栏")
        else:
            self.toc_list.show()
            self.toggle_toc_btn.setText("收起目录栏")

    def undo_text(self):
        self.text_edit.undo()

    def redo_text(self):
        self.text_edit.redo()

    def insert_divider(self):
        self.text_edit.insertPlainText("\n--------------------------\n")

    def insert_paragraph(self):
        self.text_edit.insertPlainText("\n新段落：\n")

    def update_word_count(self):
        text = self.text_edit.toPlainText()
        word_count = len(text)
        self.word_count_label.setText(f"字数：{word_count}")

        # 每次文本改动都更新目录
        self.generate_table_of_contents()

    def save_as_docx(self):
        try:
            from docx import Document
        except ImportError:
            QMessageBox.warning(self, "依赖缺失", "请先安装 python-docx：pip install python-docx")
            return

        content = self.text_edit.toPlainText()
        file_path, _ = QFileDialog.getSaveFileName(self, "保存为 DOCX", "", "Word Files (*.docx)")
        if file_path:
            try:
                doc = Document()
                doc.add_paragraph(content)
                doc.save(file_path)
                QMessageBox.information(self, "成功", "DOCX 文件保存成功！")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"保存失败: {str(e)}")

    def export_as_pdf(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "导出为 PDF", "", "PDF Files (*.pdf)")
        if file_path:
            printer = QPrinter(QPrinter.HighResolution)
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setOutputFileName(file_path)
            self.text_edit.document().print_(printer)
            QMessageBox.information(self, "导出成功", f"文件已保存为：{file_path}")

    def save_as_txt(self):
        content = self.text_edit.toPlainText()
        file_path, _ = QFileDialog.getSaveFileName(self, "保存为 TXT", "", "Text Files (*.txt)")
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                QMessageBox.information(self, "成功", "TXT 文件保存成功！")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"保存失败: {str(e)}")

    def load_file(self, file_path):
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

    def generate_table_of_contents(self):
        self.toc_list.clear()
        self.heading_positions = []

        doc = self.text_edit.document()
        block = doc.firstBlock()

        # 编译正则表达式
        pattern_chinese_num = re.compile(r'^[一二三四五六七八九十]+[、.]')
        pattern_english_num = re.compile(r'^\d+(\.\d+)*')
        pattern_chapter = re.compile(r'^第[一二三四五六七八九十\d]+章')

        while block.isValid():
            text = block.text().strip()
            if pattern_chinese_num.match(text) or pattern_english_num.match(text) or pattern_chapter.match(text):
                item = QListWidgetItem(text)
                self.toc_list.addItem(item)
                self.heading_positions.append(block.position())
            block = block.next()

    def scroll_to_heading(self, item):
        index = self.toc_list.row(item)
        if index < len(self.heading_positions):
            position = self.heading_positions[index]
            cursor = self.text_edit.textCursor()
            cursor.setPosition(position)
            self.text_edit.setTextCursor(cursor)

    def save_as_html(self):
        html_text = self.text_edit.toHtml()
        file_path, _ = QFileDialog.getSaveFileName(self, "导出为 HTML", "", "HTML 文件 (*.html)")
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(html_text)
                QMessageBox.information(self, "成功", "已成功导出为 HTML 文件")
            except Exception as e:
                QMessageBox.warning(self, "错误", f"导出失败: {str(e)}")

    def call_ai_writer(self, mode):
        from ai_writer_thread import AIWriterThread
        cursor = self.text_edit.textCursor()
        prompt = cursor.selectedText().strip()
        if not prompt:
            QMessageBox.warning(self, "提示", "请先选中需要处理的文字")
            return
        self.show_loading()  # ✅ 显示沙漏
        self.ai_thread = AIWriterThread(mode, prompt)  # 注意顺序：模式，内容
        self.ai_thread.result_signal.connect(self.insert_ai_result)
        self.ai_thread.error_signal.connect(self.show_ai_error)
        self.ai_thread.start()

    def run_ai_task(self, text, mode):
        self.setEnabled(False)
        self.statusBarMessage(f"AI 正在{mode}中...")
        self.show_loading()  # ✅ 显示沙漏
        self.ai_thread = AIWriterThread(text, mode)  # 传入模式
        self.ai_thread.result_signal.connect(self.insert_ai_result)
        self.ai_thread.error_signal.connect(self.show_ai_error)
        self.ai_thread.start()

    def insert_ai_result(self, result):
        self.hide_loading()  # ✅ 隐藏沙漏
        dialog = AIResultDialog(result, self)
        dialog.exec_()

        self.statusBarMessage("AI 处理完成 ✅")
        self.setEnabled(True)

    def show_ai_error(self, error_msg):
        self.hide_loading()  # ✅ 隐藏沙漏
        QMessageBox.warning(self, "AI 处理出错", error_msg)
        self.statusBarMessage("AI 处理失败 ❌")
        self.setEnabled(True)

    def statusBarMessage(self, message):
        self.word_count_label.setText(f"{message} | 当前字数：{len(self.text_edit.toPlainText())}")

    def show_loading(self):
        self.loading_label.show()
        self.loading_movie.start()

    def hide_loading(self):
        self.loading_movie.stop()
        self.loading_label.hide()
