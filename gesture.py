# gesture.py
import cv2
import mediapipe as mp
from PyQt5.QtCore import QThread, pyqtSignal


class HandGestureThread(QThread):
    # 创建信号用于传递识别到的手势名称
    gesture_detected = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        # 初始化 Mediapipe 手部检测模块
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,  # 动态检测（适合实时视频）
            max_num_hands=1,          # 最多检测一只手
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.running = True  # 控制线程运行状态

    def detect_gesture(self, landmarks):
        """通过关键点判断手势"""
        if not landmarks:
            return "No Hand"

        tips_ids = [4, 8, 12, 16, 20]
        fingers = []

        # 拇指：x坐标判断（左右）
        if landmarks[tips_ids[0]].x < landmarks[tips_ids[0] - 1].x:
            fingers.append(1)
        else:
            fingers.append(0)

        # 其余四指：y坐标判断（上翘/弯曲）
        for i in range(1, 5):
            if landmarks[tips_ids[i]].y < landmarks[tips_ids[i] - 2].y:
                fingers.append(1)
            else:
                fingers.append(0)

        total_fingers = sum(fingers)

        # 根据 fingers 状态判断具体手势
        if fingers == [0, 1, 0, 0, 0]:
            return "Index Finger"
        elif fingers == [0, 1, 1, 0, 0]:
            return "Scissor"
        elif total_fingers == 5:
            return "Open Palm"
        elif total_fingers == 0:
            return "Fist"
        elif fingers == [1, 0, 0, 0, 1]:
            return "Rock Gesture"
        else:
            return f"{total_fingers} Finger(s)"

    def run(self):
        """线程运行主函数：打开摄像头并实时识别手势"""
        cap = cv2.VideoCapture(0)

        while self.running:
            success, frame = cap.read()
            if not success:
                continue

            # 镜像翻转
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = self.hands.process(rgb_frame)

            gesture_name = "No Hand Detected"

            if result.multi_hand_landmarks:
                for hand_landmarks in result.multi_hand_landmarks:
                    self.mp_drawing.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                    gesture_name = self.detect_gesture(hand_landmarks.landmark)

            # 发出信号，将识别结果发送给主程序
            self.gesture_detected.emit(gesture_name)

            # 显示图像（调试用）
            cv2.putText(frame, gesture_name, (10, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow("Gesture Recognition", frame)

            # 按 q 键退出调试界面
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def stop(self):
        """停止线程"""
        self.running = False
        self.quit()
        self.wait()

