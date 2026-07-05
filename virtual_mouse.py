import cv2
import numpy as np
import pyautogui
import time
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from cvzone.HandTrackingModule import HandDetector

# -----------------------------
# Camera Settings
# -----------------------------
wCam, hCam = 640, 480
frameR = 100
smoothening = 7

# -----------------------------
# Webcam
# -----------------------------
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

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
# Screen Size
# -----------------------------
screenW, screenH = pyautogui.size()
# -----------------------------
# Volume Control Setup
# -----------------------------
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_,
    CLSCTX_ALL,
    None
)

volume = cast(interface, POINTER(IAudioEndpointVolume))

volRange = volume.GetVolumeRange()

minVol = volRange[0]
maxVol = volRange[1]
# -----------------------------
# Variables
# -----------------------------
plocX, plocY = 0, 0
clocX, clocY = 0, 0

drag = False
clickDelay = 0

# -----------------------------
# Main Loop
# -----------------------------
while True:

    success, img = cap.read()

    if not success:
        break

    img = cv2.flip(img, 1)

    hands, img = detector.findHands(img)

    cv2.rectangle(
        img,
        (frameR, frameR),
        (wCam-frameR, hCam-frameR),
        (255, 0, 255),
        2
    )

    if hands:

        hand = hands[0]

        lmList = hand["lmList"]

        fingers = detector.fingersUp(hand)

        x1, y1, _ = lmList[8]
        x2, y2, _ = lmList[12]

        # ---------------------------------
        # MOVE MOUSE
        # ---------------------------------
        if fingers == [0, 1, 0, 0, 0]:

            x3 = np.interp(
                x1,
                (frameR, wCam-frameR),
                (0, screenW)
            )

            y3 = np.interp(
                y1,
                (frameR, hCam-frameR),
                (0, screenH)
            )

            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening

            pyautogui.moveTo(clocX, clocY)

            plocX = clocX
            plocY = clocY

            cv2.putText(
                img,
                "MOVE",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                3
            )

        # ---------------------------------
        # LEFT CLICK
        # ---------------------------------
        elif fingers == [0, 1, 1, 0, 0]:

            length, info, img = detector.findDistance(
                lmList[8][:2],
                lmList[12][:2],
                img
            )

            if length < 35:

                if time.time() - clickDelay > 0.4:

                    pyautogui.click()

                    clickDelay = time.time()

            cv2.putText(
                img,
                "LEFT CLICK",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 0),
                3
            )

        # ---------------------------------
        # RIGHT CLICK
        # ---------------------------------
        elif fingers == [1, 1, 1, 0, 0]:

            length, info, img = detector.findDistance(
                lmList[4][:2],
                lmList[12][:2],
                img
            )

            if length < 35:

                if time.time() - clickDelay > 0.5:

                    pyautogui.rightClick()

                    clickDelay = time.time()

            cv2.putText(
                img,
                "RIGHT CLICK",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 0, 0),
                3
            )

        # ---------------------------------
        # DOUBLE CLICK
        # ---------------------------------
        elif fingers == [1, 0, 0, 0, 1]:

            length, info, img = detector.findDistance(
                lmList[4][:2],
                lmList[20][:2],
                img
            )

            if length < 35:

                if time.time() - clickDelay > 0.5:

                    pyautogui.doubleClick()

                    clickDelay = time.time()

            cv2.putText(
                img,
                "DOUBLE CLICK",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 255),
                3
            )

        # ---------------------------------
        # SCROLL UP
        # ---------------------------------
        elif fingers == [0, 1, 0, 0, 1]:
            pyautogui.scroll(100)
            cv2.putText(
                img,
                "SCROLL UP",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 255),
                3
            )  

            time.sleep(0.1)
        # ---------------------------------
        # SCROLL DOWN
        # ---------------------------------
        elif fingers == [0, 0, 1, 0, 1]:
            pyautogui.scroll(-100)

            cv2.putText(
                img,
                "SCROLL DOWN",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 255),
                3
            )

            time.sleep(0.1)
        # ---------------------------------
        # VOLUME CONTROL
        # Thumb + Index Up
        # ---------------------------------
        elif fingers == [1, 1, 0, 0, 0]:
            length, info, img = detector.findDistance(
            lmList[4][:2],
            lmList[8][:2],
            img
            )

            vol = np.interp(length, [20, 180], [minVol, maxVol])

            volBar = np.interp(length, [20, 180], [400, 150])

            volPer = np.interp(length, [20, 180], [0, 100])

            volume.SetMasterVolumeLevel(vol, None)

            cv2.rectangle(img, (50,150), (85,400), (0,255,0), 3)

            cv2.rectangle(
                img,
                (50, int(volBar)),
                (85,400),
                (0,255,0),
                cv2.FILLED
            )

            cv2.putText(
                img,
                f'{int(volPer)}%',
                (40,430),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255,0,0),
                3
            )

            cv2.putText(
                img,
                "VOLUME",
                (20,40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255,0,255),
                3
            )
        # ---------------------------------
        # DRAG START (Closed Fist)
        # ---------------------------------
        elif fingers == [0, 0, 0, 0, 0]:
            if not drag:
                pyautogui.mouseDown()
                drag = True

            cv2.putText(
                img,
                "DRAG",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                3
            )

        # ---------------------------------
        # RELEASE DRAG
        # ---------------------------------
        else:

            if drag:

                pyautogui.mouseUp()

                drag = False

    cv2.imshow("AI Virtual Mouse", img)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()