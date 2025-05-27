import cv2
import mediapipe as mp
from gesture import open_voice_input, exit_program, mouse_click, next_page
import time

# 初始化 Mediapipe 模块
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)

# 定义手势判断函数
def detect_gesture(landmarks):
    if not landmarks:
        return "No Hand"

    tips_ids = [4, 8, 12, 16, 20]
    fingers = []

    # 拇指（横向判断）
    if landmarks[tips_ids[0]].x < landmarks[tips_ids[0] - 1].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # 其余四指（纵向判断）
    for id in range(1, 5):
        if landmarks[tips_ids[id]].y < landmarks[tips_ids[id] - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    total_fingers = sum(fingers)

    if fingers == [0, 1, 0, 0, 0]:
        return "Point (Index)"
    elif fingers == [0, 1, 1, 0, 0]:
        return "Scissor (2 fingers)"
    elif total_fingers == 5:
        return "Open Palm"
    elif total_fingers == 0:
        return "Fist"
    elif fingers == [1, 0, 0, 0, 1]:
        return "Rock Gesture"
    elif fingers == [0, 1, 1, 1, 1]:
        return "Four Fingers"
    elif fingers == [0, 0, 1, 0, 0]:
        return "Bad Gesture"
    else:
        return f"{total_fingers} Finger(s)"

# 添加节流机制，避免重复快速触发功能
last_action_time = 0
action_cooldown = 1.5  # 秒

def handle_gesture(gesture_name):
    global last_action_time
    now = time.time()
    if now - last_action_time < action_cooldown:
        return  # 还在冷却时间内，不执行动作

    if gesture_name == "Open Palm":
        open_voice_input()
        last_action_time = now
    elif gesture_name == "Fist":
        exit_program()
        last_action_time = now
    elif gesture_name == "Point (Index)":
        mouse_click()
        last_action_time = now
    elif gesture_name == "Scissor (2 fingers)":
        next_page()
        last_action_time = now

# 打开摄像头
cap = cv2.VideoCapture(0)

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    gesture_name = "No Hand Detected"

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            gesture_name = detect_gesture(hand_landmarks.landmark)
            handle_gesture(gesture_name)  # 这里调用动作处理函数

    # 显示手势名称
    cv2.putText(frame, gesture_name, (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    cv2.imshow("Gesture Recognition", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

