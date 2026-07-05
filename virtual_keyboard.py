import cv2
import time
from cvzone.HandTrackingModule import HandDetector
from pynput.keyboard import Controller,Key

# -----------------------------
# Camera
# -----------------------------
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# -----------------------------
# Hand Detector
# -----------------------------
detector = HandDetector(
    maxHands=1,
    detectionCon=0.8
)

# -----------------------------
# Keyboard Controller
# -----------------------------
keyboard = Controller()
clickTime = 0
finalText = ""

# -----------------------------
# Button Class
# -----------------------------
class Button:
    def __init__(self, pos, text, size=(70, 70)):
        self.pos = pos
        self.text = text
        self.size = size

# -----------------------------
# Keyboard Layout
# -----------------------------
keys = [
    ["Q","W","E","R","T","Y","U","I","O","P"],
    ["A","S","D","F","G","H","J","K","L"],
    ["Z","X","C","V","B","N","M"],
    ["SPACE","BACK","ENTER"]
]

buttonList = []

# First Row
for i, key in enumerate(keys[0]):
    buttonList.append(Button((50 + i*100, 100), key))

# Second Row
for i, key in enumerate(keys[1]):
    buttonList.append(Button((100 + i*100, 200), key))

# Third Row
for i, key in enumerate(keys[2]):
    buttonList.append(Button((200 + i*100, 300), key))

# Last Row
buttonList.append(Button((150, 420), "SPACE", (300,70)))
buttonList.append(Button((500, 420), "BACK", (180,70)))
buttonList.append(Button((720, 420), "ENTER", (180,70)))

# -----------------------------
# Draw Keyboard
# -----------------------------
def drawKeyboard(img):

    for button in buttonList:

        x, y = button.pos
        w, h = button.size

        cv2.rectangle(
            img,
            (x, y),
            (x+w, y+h),
            (255,0,255),
            cv2.FILLED
        )

        cv2.rectangle(
            img,
            (x, y),
            (x+w, y+h),
            (255,255,255),
            2
        )

        cv2.putText(
            img,
            button.text,
            (x+10, y+45),
            cv2.FONT_HERSHEY_PLAIN,
            2,
            (255,255,255),
            2
        )

# -----------------------------
# Main Loop
# -----------------------------
while True:

    success, img = cap.read()

    if not success:
        break

    img = cv2.flip(img, 1)

    hands, img = detector.findHands(img)

    drawKeyboard(img)

    # -----------------------------
    # Hover Detection
    # -----------------------------
    if hands:
        hand = hands[0]

        lmList = hand["lmList"]
        fingers = detector.fingersUp(hand)

        x, y, _ = lmList[8]      # Index Finger Tip

        # Draw fingertip
        cv2.circle(img, (x, y), 12, (0, 0, 255), cv2.FILLED)

        for button in buttonList:
            bx, by = button.pos
            bw, bh = button.size

            if bx < x < bx + bw and by < y < by + bh:
                # Highlight hovered key
                cv2.rectangle(
                    img,
                    (bx, by),
                    (bx + bw, by + bh),
                    (0, 255, 0),
                    cv2.FILLED
                )

                cv2.rectangle(
                    img,
                    (bx, by),
                    (bx + bw, by + bh),
                    (255, 255, 255),
                    2
                )

                cv2.putText(
                    img,
                    button.text,
                    (bx + 10, by + 45),
                    cv2.FONT_HERSHEY_PLAIN,
                    2,
                    (0, 0, 0),
                    2
                )

                # Detect pinch
                if fingers[1] == 1 and fingers[2] == 1:

                    length, info, img = detector.findDistance(
                        lmList[8][:2],
                        lmList[12][:2],
                        img
                    )

                    if length < 35 and time.time() - clickTime > 0.5:

                        clickTime = time.time()

                        key = button.text

                        if key == "SPACE":

                            keyboard.press(" ")
                            keyboard.release(" ")

                            finalText += " "

                        elif key == "BACK":

                            keyboard.press(Key.backspace)
                            keyboard.release(Key.backspace)

                            finalText = finalText[:-1]

                        elif key == "ENTER":

                            keyboard.press(Key.enter)
                            keyboard.release(Key.enter)

                            finalText += "\n"

                        else:

                            keyboard.press(key.lower())
                            keyboard.release(key.lower())

                            finalText += key

                        time.sleep(0.15)
    cv2.rectangle(img, (40, 20), (1240, 70), (50, 50, 50), cv2.FILLED)

    cv2.putText(
        img,
        finalText,
        (60, 55),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 255, 255),
        2
    )
    cv2.imshow("AI Virtual Keyboard", img)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()