import cv2
import numpy as np
import pyautogui
from cvzone.HandTrackingModule import HandDetector

################################
wCam, hCam = 640, 480
frameR = 100
smoothening = 7
################################

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = HandDetector(maxHands=1)

screenW, screenH = pyautogui.size()

plocX, plocY = 0, 0
clocX, clocY = 0, 0

while True:

    success, img = cap.read()
    img = cv2.flip(img, 1)

    hands, img = detector.findHands(img)

    cv2.rectangle(img, (frameR, frameR),
                  (wCam-frameR, hCam-frameR),
                  (255, 0, 255), 2)

    if hands:

        hand = hands[0]
        lmList = hand["lmList"]

        x1, y1, _ = lmList[8]   # Index finger
        x2, y2, _ = lmList[12]  # Middle finger

        fingers = detector.fingersUp(hand)

        # Move Mouse (Only Index Finger Up)
        if fingers[1] == 1 and fingers[2] == 0:

            x3 = np.interp(x1, (frameR, wCam-frameR), (0, screenW))
            y3 = np.interp(y1, (frameR, hCam-frameR), (0, screenH))

            clocX = plocX + (x3-plocX)/smoothening
            clocY = plocY + (y3-plocY)/smoothening

            pyautogui.moveTo(clocX, clocY)

            cv2.circle(img, (x1, y1), 12, (255, 0, 255), cv2.FILLED)

            plocX, plocY = clocX, clocY

        # Left Click (Index + Middle Finger Up)
        if fingers[1] == 1 and fingers[2] == 1:

            length, info, img = detector.findDistance(
                   lmList[8][:2], lmList[12][:2], img)

            if length < 40:
                cv2.circle(img,
                           (info[4], info[5]),
                           15,
                           (0, 255, 0),
                           cv2.FILLED)

                pyautogui.click()

    cv2.imshow("AI Virtual Mouse", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()