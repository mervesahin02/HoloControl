import cv2
import mediapipe as mp
import numpy as np
import pyautogui
import time

# MediaPipe ayarları
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Kamera
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Yardımcı değişkenler
last_click_time = 0
last_tab_time = 0
last_right_time = 0
last_index_x = 0

# Mesafe hesaplama
def distance(p1, p2):
    return np.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

# Parmak açık mı?
def fingers_up(hand_landmarks):
    tips_ids = [4, 8, 12, 16, 20]
    fingers = []
    for i in range(1, 5):
        fingers.append(hand_landmarks.landmark[tips_ids[i]].y < hand_landmarks.landmark[tips_ids[i] - 2].y)
    thumb_tip = hand_landmarks.landmark[tips_ids[0]]
    thumb_ip = hand_landmarks.landmark[tips_ids[0] - 1]
    fingers.insert(0, thumb_tip.x < thumb_ip.x)
    return fingers

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    h, w, _ = img.shape

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Koordinatlar
            thumb = hand_landmarks.landmark[4]
            index = hand_landmarks.landmark[8]
            cx, cy = int(index.x * w), int(index.y * h)

            # Parmak durumu
            fingers = fingers_up(hand_landmarks)

            # Tıklama Jest (işaret+başparmak)
            if distance(thumb, index) < 0.04:
                if time.time() - last_click_time > 1:
                    pyautogui.click()
                    last_click_time = time.time()
                    cv2.putText(img, "Click", (cx, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Mouse hareketi (avuç açık)
            if all(fingers):
                screen_w, screen_h = pyautogui.size()
                mouse_x = np.interp(cx, [0, w], [0, screen_w])
                mouse_y = np.interp(cy, [0, h], [0, screen_h])
                pyautogui.moveTo(mouse_x, mouse_y, duration=0.1)
                cv2.putText(img, "Mouse Mode", (cx, cy - 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)

            # Alt+Tab Jest (yumruk)
            if fingers == [False, False, False, False, False]:
                if time.time() - last_tab_time > 2:
                    pyautogui.hotkey('alt', 'tab')
                    last_tab_time = time.time()
                    cv2.putText(img, "Alt+Tab", (cx, cy - 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

            # İşaret sağa kaydıysa → sağ ok
            # İşaret sağa kaydıysa → sağ ok
            if index.x - last_index_x > 0.07:
                if time.time() - last_right_time > 1:
                    pyautogui.press('right')
                    last_right_time = time.time()
                    cv2.putText(img, "Right Arrow", (cx, cy - 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
            last_index_x = index.x

            if index.x - last_index_x > 0.07:  # 0.07 hassasiyet
                if time.time() - last_right_time > 1:
                    pyautogui.press('right')
                    last_right_time = time.time()
                    cv2.putText(img, "Right Arrow", (cx, cy - 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
            last_index_x = index.x

    cv2.imshow("Gesture Control", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
