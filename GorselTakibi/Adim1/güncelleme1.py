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
    ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
    ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
    ["Z", "X", "C", "V", "B", "N", "M", "Space", "Back", "Enter"]
]

key_locations = []
key_w, key_h = 85, 85
for i, row in enumerate(keys):
    for j, key in enumerate(row):
        x = j * (key_w + 5) + 100
        y = i * (key_h + 5) + 100
        key_locations.append((key, x, y))

text = ""
last_key = ""
pressed = False


def draw_keyboard(img):
    for key, x, y in key_locations:
        color = (180, 0, 180)
        cv2.rectangle(img, (x, y), (x + key_w, y + key_h), color, cv2.FILLED)
        label = {"Space": "␣", "Back": "⌫", "Enter": "⏎"}.get(key, key)
        cv2.putText(img, label, (x + 20, y + 55), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)

hover_key = None
frame_counter = 0
hover_threshold = 15  # kaç frame beklesin

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    draw_keyboard(img)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            fingertip = hand_landmarks.landmark[8]  # İşaret parmağı ucu
            h, w, _ = img.shape
            cx, cy = int(fingertip.x * w), int(fingertip.y * h)

            # İşaretçiyi çiz
            cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)

            key_pressed = None
            for key, x, y in key_locations:
                if x < cx < x + key_w and y < cy < y + key_h:
                    key_pressed = key
                    cv2.rectangle(img, (x, y), (x + key_w, y + key_h), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, key[0], (x + 20, y + 55), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)

                    if key_pressed:
                        if key_pressed == hover_key:
                            frame_counter += 1
                        else:
                            hover_key = key_pressed
                            frame_counter = 1

                        if frame_counter >= hover_threshold:
                            if key_pressed == "Space":
                                text += " "
                            elif key_pressed == "Back":
                                text = text[:-1]
                            elif key_pressed == "Enter":
                                text += "\n"
                            else:
                                text += key_pressed
                            last_key = key_pressed
                            pressed = True
                            frame_counter = 0  # Aynı tuş tekrar yazılmasın
                    else:
                        hover_key = None
                        frame_counter = 0
                        pressed = False


            else:
                pressed = False

    # Yazılan metin kutusu
    cv2.rectangle(img, (100, 500), (1180, 600), (0, 0, 0), cv2.FILLED)
    yazi_satiri = text.split('\n')[-1]
    cv2.putText(img, yazi_satiri, (110, 570), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

    cv2.imshow("Virtual Keyboard", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
