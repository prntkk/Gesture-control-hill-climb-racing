import cv2
import mediapipe as mp
from pynput.keyboard import Controller, Key
import time

# Initialize keyboard and MediaPipe
keyboard = Controller()
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

# Flags for key press
accelerating = False
braking = False

def is_open_palm(landmarks):
    """Returns True if hand is open (fingers spread)."""
    fingers = []
    # Thumb
    fingers.append(landmarks[4].x < landmarks[3].x)
    # Other 4 fingers
    for tip in [8, 12, 16, 20]:
        fingers.append(landmarks[tip].y < landmarks[tip - 2].y)
    return all(fingers)

def is_fist(landmarks):
    """Returns True if fingers are curled (fist)."""
    for tip in [8, 12, 16, 20]:
        if landmarks[tip].y < landmarks[tip - 2].y:
            return False
    return True

cap = cv2.VideoCapture(0)

print("[INFO] Gesture control started. Use Open Palm to accelerate, Fist to brake.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Flip image and convert to RGB
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            landmarks = hand_landmarks.landmark

            if is_open_palm(landmarks):
                if not accelerating:
                    print("Accelerating 🚗")
                    keyboard.press(Key.right)
                    accelerating = True
                braking = False
                keyboard.release(Key.left)

            elif is_fist(landmarks):
                if not braking:
                    print("Braking ⛔")
                    keyboard.press(Key.left)
                    braking = True
                accelerating = False
                keyboard.release(Key.right)

            else:
                if accelerating:
                    keyboard.release(Key.right)
                    accelerating = False
                if braking:
                    keyboard.release(Key.left)
                    braking = False

    else:
        # No hand detected, release keys
        if accelerating:
            keyboard.release(Key.right)
            accelerating = False
        if braking:
            keyboard.release(Key.left)
            braking = False

    cv2.imshow("Hand Gesture Control", frame)
    if cv2.waitKey(1) & 0xFF == 27:  # Press Esc to exit
        break

cap.release()
cv2.destroyAllWindows()
