import cv2
from cvzone.HandTrackingModule import HandDetector
from pynput.keyboard import Controller

# -----------------------------
# Webcam
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

# -----------------------------
# Button Class
# -----------------------------
class Button():
    def __init__(self, pos, text, size=[70,70]):
        self.pos = pos
        self.size = size
        self.text = text

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

for i in range(len(keys)):
    for j, key in enumerate(keys[i]):

        if key == "SPACE":
            buttonList.append(Button([150,100*i+100],key,[350,70]))

        elif key == "BACK":
            buttonList.append(Button([530,100*i+100],key,[180,70]))

        elif key == "ENTER":
            buttonList.append(Button([740,100*i+100],key,[180,70]))

        else:
            buttonList.append(Button([100*j+50,100*i+100],key))

# -----------------------------
# Draw Keyboard
# -----------------------------
def drawAll(img, buttonList):

    for button in buttonList:

        x,y = button.pos
        w,h = button.size

        cv2.rectangle(
            img,
            (x,y),
            (x+w,y+h),
            (255,0,255),
            cv2.FILLED
        )

        cv2.rectangle(
            img,
            (x,y),
            (x+w,y+h),
            (255,255,255),
            3
        )

        cv2.putText(
            img,
            button.text,
            (x+15,y+45),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255,255,255),
            2
        )

    return img

# -----------------------------
# Typed Text
# -----------------------------
finalText = ""
# -----------------------------
# Main Loop
# -----------------------------
while True:

    success, img = cap.read()

    if not success:
        break

    img = cv2.flip(img, 1)

    # Detect Hands
    hands, img = detector.findHands(img)

    # Draw Keyboard
    img = drawAll(img, buttonList)

    # Display Typed Text Box
    cv2.rectangle(img, (40, 20), (1240, 80), (50, 50, 50), cv2.FILLED)
    cv2.putText(
        img,
        finalText,
        (60, 65),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.2,
        (255, 255, 255),
        2
    )

    # -----------------------------
    # Detect Finger Position
    # -----------------------------
    if hands:

        hand = hands[0]
        lmList = hand["lmList"]

        # Index fingertip
        x, y, _ = lmList[8]

        # Highlight key when hovering
        for button in buttonList:

            bx, by = button.pos
            bw, bh = button.size

            if bx < x < bx + bw and by < y < by + bh:

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
                    3
                )

                cv2.putText(
                    img,
                    button.text,
                    (bx + 15, by + 45),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 0),
                    2
                )

        # Show fingertip
        cv2.circle(img, (x, y), 10, (0, 0, 255), cv2.FILLED)

    # Show Window
    cv2.imshow("AI Virtual Keyboard", img)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()