# ui/main_window.py (完整替换)

import sys
from PyQt5.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QStackedWidget, 
                             QApplication, QGraphicsOpacityEffect, QMessageBox,
                             QAction, QFileDialog) # 新增导入
from PyQt5.QtCore import QTimer, QPropertyAnimation, QEasingCurve, pyqtSignal, Qt

# 导入所有需要的自定义模块
from ui.side_bar import Sidebar
from ui.welcome_page import WelcomePage
from ui.writing_page import WritingPage
from ui.translate_page import TranslatePage
from ui.voice_page import VoicePage
from ui.loading_overlay import LoadingOverlay

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_theme = 'dark'
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("交互式写作平台")
        self.resize(1600, 900)
        self.setMinimumSize(1024, 768)
        self.center_window()
        
        # --- 新增：创建菜单栏 ---
        self._create_menus()
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.sidebar = Sidebar()
        self.stacked_widget = QStackedWidget()
        
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.stacked_widget)

        self._init_pages()
        self.loading_overlay = LoadingOverlay(self.stacked_widget)
        self._connect_signals()
        
        self.apply_theme()
        self.stacked_widget.setCurrentWidget(self.page_map['welcome'])
        self.sidebar.hide()

    def _create_menus(self):
        """创建顶部菜单栏。"""
        menu_bar = self.menuBar()

        # 文件菜单
        file_menu = menu_bar.addMenu("文件")
        open_action = QAction("打开...", self)
        open_action.triggered.connect(self._open_file_and_write)
        file_menu.addAction(open_action)
        file_menu.addSeparator()
        exit_action = QAction("退出", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 视图菜单
        view_menu = menu_bar.addMenu("视图")
        theme_action = QAction("切换深/浅色主题", self)
        theme_action.triggered.connect(self._toggle_theme_and_apply)
        view_menu.addAction(theme_action)
        
        # 帮助菜单
        help_menu = menu_bar.addMenu("帮助")
        about_action = QAction("关于", self)
        about_action.triggered.connect(lambda: QMessageBox.information(self, "关于", "交互式写作平台 v1.1"))
        help_menu.addAction(about_action)

    def _init_pages(self):
        # ... (此方法无变化) ...
        self.page_map = {
            'welcome': WelcomePage(),
            'writer': WritingPage(),
            'translate': TranslatePage(),
            'voice': VoicePage(),
        }
        for page in self.page_map.values():
            self.stacked_widget.addWidget(page)
            effect = QGraphicsOpacityEffect(page)
            page.setGraphicsEffect(effect)
            page.opacity_anim = QPropertyAnimation(effect, b"opacity")
            page.opacity_anim.setDuration(250)

    def _connect_signals(self):
        """连接所有信号，包括新增的。"""
        self.sidebar.navigation_requested.connect(self._switch_page)
        self.sidebar.settings_requested.connect(self._toggle_theme_and_apply)
        
        # 欢迎页信号
        welcome_page = self.page_map['welcome']
        welcome_page.start_creation.connect(self._enter_main_workspace)
        welcome_page.open_txt_file.connect(self._open_file_and_write)
        welcome_page.exit_app.connect(self.close)

        # 写作页信号
        self.page_map['writer'].ai_request.connect(self._handle_ai_request)

    def center_window(self):
        # ... (此方法无变化) ...
        screen_geometry = QApplication.desktop().screenGeometry()
        self.move(
            (screen_geometry.width() - self.width()) // 2,
            (screen_geometry.height() - self.height()) // 2
        )

    def _switch_page(self, name):
        # ... (此方法无变化) ...
        current_widget = self.stacked_widget.currentWidget()
        target_widget = self.page_map.get(name)
        if not target_widget or current_widget == target_widget:
            return
        try:
            current_widget.opacity_anim.finished.disconnect()
        except TypeError:
            pass
        current_widget.opacity_anim.setStartValue(1)
        current_widget.opacity_anim.setEndValue(0)
        target_widget.opacity_anim.setStartValue(0)
        target_widget.opacity_anim.setEndValue(1)
        def on_fade_out_finished():
            self.stacked_widget.setCurrentWidget(target_widget)
            target_widget.opacity_anim.start()
            current_widget.opacity_anim.finished.disconnect(on_fade_out_finished)
        current_widget.opacity_anim.finished.connect(on_fade_out_finished)
        current_widget.opacity_anim.start()

    def _enter_main_workspace(self):
        self.sidebar.show()
        self._switch_page('writer')

    # --- 新增：处理文件打开和主题切换的方法 ---
    def _open_file_and_write(self):
        """弹出文件对话框，读取内容并进入写作页面。"""
        file_path, _ = QFileDialog.getOpenFileName(self, "打开 TXT 文件", "", "文本文件 (*.txt)")
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                # 将内容设置到写作页的输入框
                self.page_map['writer'].set_input_text(content)
                # 直接进入工作区
                self._enter_main_workspace()
            except Exception as e:
                QMessageBox.critical(self, "打开失败", f"无法读取文件：\n{str(e)}")

    def _toggle_theme_and_apply(self):
        """切换主题状态并应用新的样式表。"""
        self.current_theme = 'light' if self.current_theme == 'dark' else 'dark'
        self.apply_theme()
    # --- 新增结束 ---

    def _handle_ai_request(self, mode, text):
        # ... (此方法无变化) ...
        if not text.strip():
            QMessageBox.warning(self, "输入为空", "请输入一些内容后再尝试AI功能。")
            return
        self.loading_overlay.show()
        QTimer.singleShot(2000, lambda: self._on_ai_finished(mode, text))

    def _on_ai_finished(self, mode, text):
        # ... (此方法无变化) ...
        result = f"这是 AI 对“{text[:30]}...”进行的【{mode}】操作的模拟结果。\n\n" \
                 f"Lorem ipsum dolor sit amet, consectetur adipiscing elit, " \
                 f"sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. " \
                 f"Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris " \
                 f"nisi ut aliquip ex ea commodo consequat."
        self.page_map['writer'].set_output_text(result)
        self.loading_overlay.hide()

    def apply_theme(self):
        # ... (此方法无变化) ...
        qss = self._get_dark_theme_qss() if self.current_theme == 'dark' else self._get_light_theme_qss()
        self.setStyleSheet(qss)
    
    def resizeEvent(self, event):
        # ... (此方法无变化) ...
        if hasattr(self, 'loading_overlay'):
            self.loading_overlay.resize(self.stacked_widget.size())
        super().resizeEvent(event)

    def _get_dark_theme_qss(self):
        """返回深色主题的QSS字符串。 (新增了次要按钮样式)"""
        return """
            QMainWindow { background-color: #1e1f22; }
            QMenuBar { background-color: #2b2d30; color: #a9b7c6; }
            QMenuBar::item:selected { background-color: #0d6efd; }
            QMenu { background-color: #2b2d30; color: #a9b7c6; border: 1px solid #4a4d52; }
            QMenu::item:selected { background-color: #0d6efd; color: white; }

            #Sidebar { background-color: #282a2e; border-right: 1px solid #3c3f44; }
            #SidebarButton {
                color: #a9b7c6; font-size: 24px; border: none; border-radius: 8px;
            }
            #SidebarButton:hover { background-color: #3c3f44; }
            #SidebarButton:checked { background-color: #0d6efd; color: white; }
            
            #WelcomePage { background-color: #1e1f22; }
            #WelcomeTitle { color: #e3e3e3; font-size: 64px; font-weight: 300; }
            #WelcomeSubtitle { color: #8c8c8c; font-size: 18px; font-weight: 300; }
            #WelcomeButton {
                font-size: 20px; font-weight: bold; color: white;
                background-color: #0d6efd; border: none;
                padding: 18px 40px; border-radius: 12px;
            }
            #WelcomeButton:hover { background-color: #3a86ff; }
            
            /* 新增的次要按钮样式 */
            #SecondaryWelcomeButton {
                font-size: 14px; color: #8c8c8c; background-color: transparent;
                border: none; padding: 5px;
            }
            #SecondaryWelcomeButton:hover { color: #e3e3e3; text-decoration: underline; }
            
            #WritingPage { background-color: #1e1f22; }
            #ActionBar { border-bottom: 1px solid #3c3f44; }
            #ActionBarTitle { color: #a9b7c6; font-size: 16px; font-weight: bold; }
            #ActionBar QPushButton {
                font-size: 15px; color: #a9b7c6; background-color: #2b2d30;
                border: 1px solid #4a4d52; padding: 8px 16px; border-radius: 8px;
            }
            #ActionBar QPushButton:hover { background-color: #3c3f44; }

            QSplitter::handle { background-color: #282a2e; }
            QSplitter::handle:hover { background-color: #0d6efd; }
            QSplitter::handle:pressed { background-color: #3a86ff; }

            QTextEdit {
                background-color: #1e1f22; color: #c3c3c3;
                border: none; font-size: 18px; 
                padding: 10px;
            }
            QTextEdit QScrollBar:vertical {
                border: none; background: #282a2e; width: 10px;
            }
            QTextEdit QScrollBar::handle:vertical {
                background: #4a4d52; border-radius: 5px; min-height: 20px;
            }
            
            #PagePlaceholderLabel { font-size: 24px; color: #6c757d; }
            #LoadingOverlay { background-color: rgba(30, 31, 34, 0.85); border-radius: 0px; }
            #LoadingLabel { color: white; font-size: 20px; font-weight: bold; }
        """
    
    def _get_light_theme_qss(self):
        """返回浅色主题的QSS字符串。 (新增了次要按钮样式)"""
        return """
            QMainWindow { background-color: #f8f9fa; }
            QMenuBar { background-color: #e9ecef; color: #212529; }
            QMenuBar::item:selected { background-color: #0d6efd; color: white; }
            QMenu { background-color: #ffffff; color: #212529; border: 1px solid #dee2e6; }
            QMenu::item:selected { background-color: #0d6efd; color: white; }

            #Sidebar { background-color: #f1f3f5; border-right: 1px solid #dee2e6; }
            #SidebarButton {
                color: #495057; font-size: 24px; border: none; border-radius: 8px;
            }
            #SidebarButton:hover { background-color: #e9ecef; }
            #SidebarButton:checked { background-color: #0d6efd; color: white; }
            
            #WelcomePage { background-color: #f8f9fa; }
            #WelcomeTitle { color: #212529; font-size: 64px; font-weight: 300; }
            #WelcomeSubtitle { color: #6c757d; font-size: 18px; font-weight: 300; }
            #WelcomeButton {
                font-size: 20px; font-weight: bold; color: white;
                background-color: #0d6efd; border: none;
                padding: 18px 40px; border-radius: 12px;
            }
            #WelcomeButton:hover { background-color: #3a86ff; }
            
            /* 新增的次要按钮样式 */
            #SecondaryWelcomeButton {
                font-size: 14px; color: #6c757d; background-color: transparent;
                border: none; padding: 5px;
            }
            #SecondaryWelcomeButton:hover { color: #212529; text-decoration: underline; }

            #WritingPage { background-color: #ffffff; }
            #ActionBar { border-bottom: 1px solid #e9ecef; }
            #ActionBarTitle { color: #343a40; font-size: 16px; font-weight: bold; }
            #ActionBar QPushButton {
                font-size: 15px; color: #495057; background-color: #f8f9fa;
                border: 1px solid #dee2e6; padding: 8px 16px; border-radius: 8px;
            }
            #ActionBar QPushButton:hover { background-color: #e9ecef; }

            QSplitter::handle { background-color: #f8f9fa; }
            QSplitter::handle:hover { background-color: #0d6efd; }
            QSplitter::handle:pressed { background-color: #3a86ff; }

            QTextEdit {
                background-color: #ffffff; color: #212529;
                border: none; font-size: 18px;
                padding: 10px;
            }
            QTextEdit QScrollBar:vertical {
                border: none; background: #f8f9fa; width: 10px;
            }
            QTextEdit QScrollBar::handle:vertical {
                background: #ced4da; border-radius: 5px; min-height: 20px;
            }
            
            #PagePlaceholderLabel { font-size: 24px; color: #adb5bd; }
            #LoadingOverlay { background-color: rgba(255, 255, 255, 0.85); border-radius: 0px; }
            #LoadingLabel { color: #212529; font-size: 20px; font-weight: bold; }
        """