import cv2
import mediapipe as mp
import numpy as np

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Tuş yapısı
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
pressed = False  # tuş basılı mı

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    # Tuşları çiz
    for key, x, y in key_locations:
        cv2.rectangle(img, (x, y), (x + key_w, y + key_h), (180, 0, 180), cv2.FILLED)
        label = "␣" if key == "Space" else "⏎" if key == "Enter" else "⌫" if key == "Back" else key
        cv2.putText(img, label, (x + 20, y + 55), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            finger_tip = hand_landmarks.landmark[8]
            h, w, c = img.shape
            cx, cy = int(finger_tip.x * w), int(finger_tip.y * h)
            cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)

            key_pressed = None
            for key, x, y in key_locations:
                if x < cx < x + key_w and y < cy < y + key_h:
                    key_pressed = key
                    cv2.rectangle(img, (x, y), (x + key_w, y + key_h), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, key[0] if key not in ["Space", "Back", "Enter"] else key, (x + 20, y + 55),
                                cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

                    # Sadece ilk kez bastığında ekle
                    if not pressed or key != last_key:
                        if key == "Space":
                            text += " "
                        elif key == "Back":
                            text = text[:-1]
                        elif key == "Enter":
                            text += "\n"
                        else:
                            text += key
                        pressed = True
                        last_key = key
                    break
            else:
                pressed = False  # hiçbir tuşun içinde değilse tuş bırakıldı

    # Yazılan metni göster
    cv2.rectangle(img, (100, 350), (1100, 450), (0, 0, 0), cv2.FILLED)
    yazi_satirlari = text.split("\n")[-1:]  # sadece son satırı göster
    cv2.putText(img, yazi_satirlari[0], (110, 430), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)

    cv2.imshow("Virtual Keyboard", img)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
