# ui/writing_page.py

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, 
                             QPushButton, QSplitter, QLabel, QFrame)
from PyQt5.QtCore import Qt, pyqtSignal

class WritingPage(QWidget):
    ai_request = pyqtSignal(str, str)  # (mode, text)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("WritingPage")
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # 1. 顶部操作栏
        action_bar = self._create_action_bar()
        main_layout.addWidget(action_bar)
        
        # 2. 编辑区分割器
        editor_splitter = self._create_editor_splitter()
        main_layout.addWidget(editor_splitter, stretch=1)

    def _create_action_bar(self):
        bar = QFrame()
        bar.setObjectName("ActionBar")
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        layout.setAlignment(Qt.AlignLeft)

        title = QLabel("AI 写作模式")
        title.setObjectName("ActionBarTitle")
        
        self.btn_continue = QPushButton("🚀 续写")
        self.btn_rewrite = QPushButton("✍️ 改写")
        self.btn_polish = QPushButton("✨ 润色")

        layout.addWidget(title)
        layout.addWidget(self.btn_continue)
        layout.addWidget(self.btn_rewrite)
        layout.addWidget(self.btn_polish)
        layout.addStretch()

        # 连接信号
        self.btn_continue.clicked.connect(lambda: self._emit_ai_request("续写"))
        self.btn_rewrite.clicked.connect(lambda: self._emit_ai_request("改写"))
        self.btn_polish.clicked.connect(lambda: self._emit_ai_request("润色"))
        
        return bar

    def _create_editor_splitter(self):
        splitter = QSplitter(Qt.Vertical)
        splitter.setHandleWidth(10) # 更宽的拖动条
        splitter.setObjectName("EditorSplitter")

        self.input_editor = QTextEdit()
        self.input_editor.setObjectName("InputEditor")
        self.input_editor.setPlaceholderText("在此处输入您的灵感，或粘贴需要处理的文本...")

        self.output_editor = QTextEdit()
        self.output_editor.setObjectName("OutputEditor")
        self.output_editor.setPlaceholderText("AI 的创作将在这里呈现...")
        self.output_editor.setReadOnly(True)

        splitter.addWidget(self.input_editor)
        splitter.addWidget(self.output_editor)
        splitter.setSizes([self.height() // 2, self.height() // 2])
        return splitter

    def _emit_ai_request(self, mode):
        text = self.input_editor.toPlainText()
        self.ai_request.emit(mode, text)
        
    def set_output_text(self, text):
        self.output_editor.setPlainText(text)
        
    def set_input_text(self, text):
        self.input_editor.setPlainText(text)