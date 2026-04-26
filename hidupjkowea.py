import cv2
import mediapipe as mp
import pygame

# inittttt dari librari pygame
pygame.mixer.init()
pygame.mixer.music.load("sound.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.pause()

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7
)

cap = cv2.VideoCapture(0)

tip_ids = [4, 8, 12, 16, 20]

is_paused = True
print("Memulai Program..., Pencet Q buat keluar")
print("By masipan")
print("github.com/promptdrake")
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    hand_detected = False

    if results.multi_hand_landmarks:
        hand_detected = True

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

  
            if total_fingers >= 4:
                if is_paused:
                    pygame.mixer.music.unpause()
                    print(True)
                    is_paused = False

         
            elif total_fingers <= 1:
                if not is_paused:
                    pygame.mixer.music.pause()
                    print(False)
                    is_paused = True


    if not hand_detected:
        if not is_paused:
            pygame.mixer.music.pause()
            print(False)
            is_paused = True

    cv2.imshow("Antek antek async", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
pygame.mixer.music.stop()
cv2.destroyAllWindows()
