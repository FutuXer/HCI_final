# ui/sidebar.py (完整替换)

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QSizePolicy
from PyQt5.QtCore import pyqtSignal, QSize, Qt
from PyQt5.QtGui import QIcon, QCursor

class Sidebar(QWidget):
    navigation_requested = pyqtSignal(str)
    settings_requested = pyqtSignal()  # --- 新增信号 ---

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(70)
        self.setObjectName("Sidebar")
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(5, 10, 5, 10)
        main_layout.setSpacing(10)
        # 注意：这里不再是 AlignTop，让伸缩项能正常工作

        # 主要导航按钮
        buttons_config = [
            ('writer', '✍️', '写作'),
            ('translate', '🌍', '翻译'),
            ('voice', '🗣️', '语音'),
        ]

        self.buttons = {}
        for name, icon, tooltip in buttons_config:
            btn = QPushButton(icon)
            btn.setObjectName("SidebarButton")
            btn.setToolTip(tooltip)
            btn.setCheckable(True)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.setFixedSize(60, 50)
            btn.setCursor(QCursor(Qt.PointingHandCursor))
            btn.clicked.connect(lambda checked, n=name: self._on_button_clicked(n))
            main_layout.addWidget(btn)
            self.buttons[name] = btn
            
        if 'writer' in self.buttons:
            self.buttons['writer'].setChecked(True)
            
        # --- 新增：底部设置按钮 ---
        main_layout.addStretch() # 添加一个伸缩项，将下面的按钮推到底部

        settings_btn = QPushButton("🎨") # 可以换成设置图标 '⚙️'
        settings_btn.setObjectName("SidebarButton") # 复用样式
        settings_btn.setToolTip("切换主题")
        settings_btn.setCheckable(False) # 它不是导航按钮，只是一个触发器
        settings_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        settings_btn.setFixedSize(60, 50)
        settings_btn.setCursor(QCursor(Qt.PointingHandCursor))
        settings_btn.clicked.connect(self.settings_requested.emit)
        main_layout.addWidget(settings_btn)
        # --- 新增结束 ---
        
    def _on_button_clicked(self, name):
        for btn_name, button in self.buttons.items():
            if btn_name != name:
                button.setChecked(False)
        self.buttons[name].setChecked(True)
        self.navigation_requested.emit(name)