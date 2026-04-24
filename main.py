import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.7
)

cap = cv2.VideoCapture(0)

tip_ids = [4, 8, 12, 16, 20]
last_count = -1

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    total_all_hands = 0

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            lm_list = hand_landmarks.landmark
            fingers = []

            
            if lm_list[tip_ids[0]].x < lm_list[tip_ids[0]-1].x:
                fingers.append(1)
            else:
                fingers.append(0)

  
            for i in range(1, 5):
                if lm_list[tip_ids[i]].y < lm_list[tip_ids[i]-2].y:
                    fingers.append(1)
                else:
                    fingers.append(0)

            total_fingers = fingers.count(1)
            total_all_hands += total_fingers

    if total_all_hands != last_count:
        print("Jari:", total_all_hands)
        last_count = total_all_hands

    cv2.imshow("Suki Liar", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
