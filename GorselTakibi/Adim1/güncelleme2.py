import cv2
import mediapipe as mp
import numpy as np

# MediaPipe el modeli
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Kamera ayarları
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Klavye tuşları
keys = [
    ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"],
    ["a", "s", "d", "f", "g", "h", "j", "k", "l"],
    ["z", "x", "c", "v", "b", "n", "m"],
    ["123", "emoji", "space", "return"]
]

# Tuş ölçüleri ve yazı verileri
key_locations = []
key_w, key_h = 85, 85
text = ""
last_key = ""
pressed = False
hover_key = None
frame_counter = 0
hover_threshold = 15  # 15 frame sabit kalırsa yaz

def draw_keyboard(img):
    global key_locations
    key_locations.clear()
    overlay = img.copy()
    alpha = 0.6
    row_offsets = [0, 50, 100, 0]  # satır kaydırma

    for i, row in enumerate(keys):
        total_width = len(row) * (key_w + 10)
        x_offset = (1280 - total_width) // 2 + row_offsets[i]
        y = i * (key_h + 20) + 80

        for j, key in enumerate(row):
            x = x_offset + j * (key_w + 10)

            if key in ["space", "return", "123", "emoji"]:
                w = key_w * 2 if key == "space" else key_w + 10
                h = key_h
                cv2.rectangle(overlay, (x, y), (x + w, y + h), (255, 255, 255), -1)
                cv2.putText(overlay, key, (x + 20, y + int(h * 0.7)), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 0), 2)
                key_locations.append((key, x, y, w, h, "rect"))
            else:
                center = (x + key_w // 2, y + key_h // 2)
                radius = key_w // 2
                cv2.circle(overlay, center, radius, (255, 255, 255), -1)
                cv2.putText(overlay, key, (x + 25, y + 55), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
                key_locations.append((key, x, y, key_w, key_h, "circle"))

    cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    draw_keyboard(img)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            fingertip = hand_landmarks.landmark[8]
            h, w, _ = img.shape
            cx, cy = int(fingertip.x * w), int(fingertip.y * h)
            cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)

            key_pressed = None
            for key, x, y, kw, kh, shape in key_locations:
                if shape == "circle":
                    dist = np.sqrt((cx - (x + kw // 2))**2 + (cy - (y + kh // 2))**2)
                    if dist < kw // 2:
                        key_pressed = key
                        break
                else:
                    if x < cx < x + kw and y < cy < y + kh:
                        key_pressed = key
                        break

            if key_pressed:
                if key_pressed == hover_key:
                    frame_counter += 1
                else:
                    hover_key = key_pressed
                    frame_counter = 1

                if frame_counter >= hover_threshold:
                    if key_pressed == "space":
                        text += " "
                    elif key_pressed == "return":
                        text += "\n"
                    elif key_pressed == "emoji":
                        text += "😊"
                    elif key_pressed == "123":
                        text += "123"
                    else:
                        text += key_pressed
                    last_key = key_pressed
                    pressed = True
                    frame_counter = 0
            else:
                hover_key = None
                frame_counter = 0
                pressed = False

    # Yazılan metni göster
    cv2.rectangle(img, (100, 500), (1180, 600), (0, 0, 0), cv2.FILLED)
    yazi_satiri = text.split('\n')[-1]
    cv2.putText(img, yazi_satiri, (110, 570), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

    cv2.imshow("Virtual Keyboard", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
