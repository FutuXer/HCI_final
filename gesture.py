# gesture_actions.py

import pyautogui
import sys
import time
import threading
import os

def open_voice_input():
    print("✅ Open Palm Detected: Opening voice input...")
    # 模拟调用语音识别模块或脚本（例如 voice_input.py）
    # threading.Thread(target=os.system, args=("python voice_input.py",)).start()
    # 为演示我们先 print
    print("🎤 Voice input started (placeholder)")

def exit_program():
    print("❌ Fist Detected: Exiting program...")
    # sys.exit(0)

def mouse_click():
    print("🖱️ Index Finger Detected: Simulating mouse click...")
    pyautogui.click()

def next_page():
    print("📄 Scissor Detected: Going to next page...")
    # 模拟按右方向键或 PageDown
    pyautogui.press('right')
