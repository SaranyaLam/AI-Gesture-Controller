import cv2
import time
import subprocess
import pyautogui
import keyboard
from cvzone.HandTrackingModule import HandDetector

# -----------------------------
# Camera Setup
# -----------------------------
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# -----------------------------
# Hand Detector
# -----------------------------
detector = HandDetector(
    staticMode=False,
    maxHands=1,
    detectionCon=0.8,
    minTrackCon=0.8
)

# -----------------------------
# Variables
# -----------------------------
lastActionTime = 0
cooldown = 2      # seconds

# -----------------------------
# Main Loop
# -----------------------------
while True:

    success, img = cap.read()

    if not success:
        break

    img = cv2.flip(img, 1)

    hands, img = detector.findHands(img)

    action = "No Gesture"

    if hands:

        hand = hands[0]

        fingers = detector.fingersUp(hand)

        currentTime = time.time()

        # -----------------------------
        # Open Chrome
        # Thumb Only
        # -----------------------------
        if fingers == [1,0,0,0,0]:

            action = "Open Chrome"

            if currentTime-lastActionTime > cooldown:

                subprocess.Popen("start chrome", shell=True)

                lastActionTime = currentTime

        # -----------------------------
        # Open Notepad
        # Index + Middle
        # -----------------------------
        elif fingers == [0,1,1,0,0]:

            action = "Open Notepad"

            if currentTime-lastActionTime > cooldown:

                subprocess.Popen("notepad")

                lastActionTime = currentTime

        # -----------------------------
        # Open Calculator
        # Index + Pinky
        # -----------------------------
        elif fingers == [0,1,0,0,1]:

            action = "Open Calculator"

            if currentTime-lastActionTime > cooldown:

                subprocess.Popen("calc")

                lastActionTime = currentTime

        # -----------------------------
        # Screenshot
        # All Fingers
        # -----------------------------
        elif fingers == [1,1,1,1,1]:

            action = "Screenshot"

            if currentTime-lastActionTime > cooldown:

                imgShot = pyautogui.screenshot()

                filename = f"screenshot_{int(currentTime)}.png"

                imgShot.save(filename)

                lastActionTime = currentTime

        # -----------------------------
        # Play / Pause
        # Closed Fist
        # -----------------------------
        elif fingers == [0,0,0,0,0]:

            action = "Play / Pause"

            if currentTime-lastActionTime > cooldown:

                keyboard.press_and_release("play/pause media")

                lastActionTime = currentTime

    # -----------------------------
    # Display Action
    # -----------------------------
    cv2.rectangle(img, (0,0), (640,60), (0,0,0), cv2.FILLED)

    cv2.putText(
        img,
        action,
        (20,40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0,255,0),
        2
    )

    cv2.imshow("Gesture Shortcuts", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()