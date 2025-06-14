import cv2
import mediapipe as mp
from PyQt5.QtCore import QThread, pyqtSignal
import time

class HandGestureThread(QThread):
    gesture_detected = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.running = True

        # 多帧缓冲区，保存最近识别的手势
        self.gesture_buffer = []
        self.buffer_size = 5  # 连续5帧稳定

        # 节流控制
        self.last_gesture = None
        self.last_trigger_time = 0
        self.trigger_interval = 0.5  # 0.5秒

    def detect_gesture(self, landmarks, is_right=True):
        if not landmarks:
            return "No Hand"

        tips_ids = [4, 8, 12, 16, 20]
        fingers = []

        # 拇指判断，左右手不同
        if is_right:
            fingers.append(1 if landmarks[tips_ids[0]].x < landmarks[tips_ids[0] - 1].x else 0)
        else:
            fingers.append(1 if landmarks[tips_ids[0]].x > landmarks[tips_ids[0] - 1].x else 0)

        # 其余4指，根据y坐标判断是否伸出
        for i in range(1, 5):
            fingers.append(1 if landmarks[tips_ids[i]].y < landmarks[tips_ids[i] - 2].y else 0)

        total_fingers = sum(fingers)

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
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Cannot open camera")
            return

        while self.running:
            success, frame = cap.read()
            if not success:
                continue

            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb_frame)

            gesture_name = "No Hand Detected"

            if results.multi_hand_landmarks:
                for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                    # 判断左右手
                    if results.multi_handedness:
                        handedness = results.multi_handedness[idx].classification[0].label
                        is_right = handedness == "Right"
                    else:
                        is_right = True  # 默认右手

                    self.mp_drawing.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                    gesture_name = self.detect_gesture(hand_landmarks.landmark, is_right)

            # 添加到缓冲区
            self.gesture_buffer.append(gesture_name)
            if len(self.gesture_buffer) > self.buffer_size:
                self.gesture_buffer.pop(0)

            # 判断缓冲区中是否连续稳定
            stable_gesture = None
            for g in set(self.gesture_buffer):
                if self.gesture_buffer.count(g) >= self.buffer_size * 0.8:
                    stable_gesture = g
                    break

            # 节流判断，间隔够才发信号
            now = time.time()
            if stable_gesture and stable_gesture != self.last_gesture and (now - self.last_trigger_time) > self.trigger_interval:
                self.gesture_detected.emit(stable_gesture)
                self.last_gesture = stable_gesture
                self.last_trigger_time = now

            # 调试显示
            cv2.putText(frame, stable_gesture or gesture_name, (10, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow("Gesture Recognition", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def stop(self):
        self.running = False
        self.wait()
