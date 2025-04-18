import cv2
import mediapipe as mp
import math
import time
from pynput.keyboard import Controller, Key

# ─── Setup ────────────────────────────────────────────────────────────────────
keyboard = Controller()
mp_hands = mp.solutions.hands
mp_draw  = mp.solutions.drawing_utils
hands    = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

# thresholds (tweak these)
TILT_THRESHOLD = 15  # degrees
BOOST_FINGERS  = 2

# state
prev_keys = set()

# ─── Helpers ──────────────────────────────────────────────────────────────────
def count_fingers(hand):
    tips = [4, 8, 12, 16, 20]
    count = 0
    # thumb: compare x against its lower joint
    if hand.landmark[4].x > hand.landmark[3].x:
        count += 1
    # other fingers: tip y above pip y
    for tip in tips[1:]:
        if hand.landmark[tip].y < hand.landmark[tip - 2].y:
            count += 1
    return count

def get_hand_tilt(hand):
    # use index_finger_mcp (5) and pinky_mcp (17)
    x1, y1 = hand.landmark[5].x, hand.landmark[5].y
    x2, y2 = hand.landmark[17].x, hand.landmark[17].y
    angle = math.degrees(math.atan2((y2 - y1), (x2 - x1)))
    # roll: 0 is flat, positive tilts right, negative tilts left
    return angle

def update_key(key, press=True):
    """Press or release a key and track state to avoid repeats."""
    if press and key not in prev_keys:
        keyboard.press(key)
        prev_keys.add(key)
    if not press and key in prev_keys:
        keyboard.release(key)
        prev_keys.remove(key)

# ─── Main Loop ────────────────────────────────────────────────────────────────
cap = cv2.VideoCapture(0)
print("[INFO] Starting gesture control. Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb   = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    res   = hands.process(rgb)

    # default: release movement keys
    update_key('w', False)
    update_key('s', False)
    update_key('a', False)
    update_key('d', False)
    update_key(Key.shift, False)

    if res.multi_hand_landmarks:
        hand = res.multi_hand_landmarks[0]
        mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

        fingers = count_fingers(hand)
        tilt    = get_hand_tilt(hand)

        # forward/back
        if fingers >= 4:
            update_key('w', True)   # accelerate
        elif fingers == 0:
            update_key('s', True)   # brake/reverse

        # boost
        if fingers == BOOST_FINGERS:
            update_key(Key.shift, True)

        # steering only when accelerating (fingers >=4)
        if fingers >= 4:
            if tilt >  TILT_THRESHOLD:
                update_key('d', True)  # steer right
            elif tilt < -TILT_THRESHOLD:
                update_key('a', True)  # steer left

    cv2.imshow("Gesture Control", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
