# ui/loading_overlay.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve

class LoadingOverlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setObjectName("LoadingOverlay")
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        
        self.loading_label = QLabel("正在处理中...")
        self.loading_label.setObjectName("LoadingLabel")
        layout.addWidget(self.loading_label)

        # 在 __init__ 中只创建动画对象，不启动
        self.opacity_anim = QPropertyAnimation(self, b"windowOpacity")
        self.opacity_anim.setDuration(300)
        self.opacity_anim.setEasingCurve(QEasingCurve.InOutQuad)
        
        super().hide() # 默认隐藏，使用父类的 hide 方法

    def show(self):
        if not self.parent():
            return
        self.resize(self.parent().size())
        super().show()
        
        # 淡入动画
        self.opacity_anim.setStartValue(0)
        self.opacity_anim.setEndValue(1)
        self.opacity_anim.start()

    def hide(self):
        # 淡出动画
        self.opacity_anim.setStartValue(1)
        self.opacity_anim.setEndValue(0)
        
        # --- 核心修正 ---
        # 必须先调用 super() 获取父类代理对象，然后再调用其 hide 方法
        # 我们将 super().hide 连接到动画完成的信号上
        try:
            self.opacity_anim.finished.disconnect()
        except TypeError:
            pass # 忽略没有连接的错误
        self.opacity_anim.finished.connect(super().hide) # <-- 正确的写法
        
        self.opacity_anim.start()