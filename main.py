import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from ui_main import Ui_MainWindow
from voice import recognize_speech
from PyQt5.QtWidgets import QSplashScreen
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QTimer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # 连接按钮事件
        self.ui.btnVoice.clicked.connect(self.handle_voice)
        self.ui.btnTranslate.clicked.connect(self.handle_translate)
        self.ui.btnAIWrite.clicked.connect(self.handle_ai_write)
        self.ui.btnGesture.clicked.connect(self.handle_gesture)

    def handle_voice(self):
        self.ui.statusLabel.setText("🎙 正在语音识别...")
        text = recognize_speech()
        self.ui.textInput.setPlainText(text)
        self.ui.statusLabel.setText("✅ 语音输入完成")

    def handle_translate(self):
        input_text = self.ui.textInput.toPlainText()
        output = f"[翻译结果模拟]：{input_text[::-1]}"
        self.ui.textOutput.setPlainText(output)
        self.ui.statusLabel.setText("✅ 翻译完成")

    def handle_ai_write(self):
        input_text = self.ui.textInput.toPlainText()
        output = input_text + "（这里是AI生成的内容扩展）"
        self.ui.textOutput.setPlainText(output)
        self.ui.statusLabel.setText("✅ AI写作完成")

    def handle_gesture(self):
        self.ui.statusLabel.setText("🖐 启动手势识别中...")
        import subprocess
        subprocess.Popen(["python", "gesture_main.py"])

class SplashScreen(QSplashScreen):
    def __init__(self):
        pixmap = QPixmap("splash_image.png")  # 你的启动页图片路径
        super().__init__(pixmap)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.showMessage("欢迎使用 AI 辅助写作与翻译平台", Qt.AlignBottom | Qt.AlignCenter, Qt.white)
        self.setFont(QFont("微软雅黑", 12))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    splash = SplashScreen()
    splash.show()

    def show_main():
        splash.close()
        win = MainWindow()
        win.show()

    QTimer.singleShot(3000, show_main)  # 3秒后自动关闭启动页，显示主界面
    sys.exit(app.exec_())


