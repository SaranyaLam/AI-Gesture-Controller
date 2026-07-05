import customtkinter as ctk
from PIL import Image, ImageTk
import cv2
import subprocess
import sys
from datetime import datetime
import psutil
import time
# -----------------------------
# Theme
# -----------------------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

# -----------------------------
# Main Window
# -----------------------------
# -----------------------------
# Launch Programs
# -----------------------------
def launch_mouse():
    subprocess.Popen([sys.executable, "virtual_mouse.py"])

def launch_keyboard():
    subprocess.Popen([sys.executable, "virtual_keyboard.py"])

def launch_shortcuts():
    subprocess.Popen([sys.executable, "gesture_shortcuts.py"])
app = ctk.CTk()
app.configure(fg_color="#08121F")

cap = cv2.VideoCapture(0)
prevTime = time.time()

app.title("AI Gesture Controller")
app.geometry("1200x700")
app.resizable(True, True)

header = ctk.CTkFrame(
    app,
    height=80,
    corner_radius=0,
    fg_color="#2563EB"
)

header.place(x=0, y=0, relwidth=1)

title = ctk.CTkLabel(
    header,
    text="🤖 AI GESTURE CONTROLLER",
    font=("Segoe UI", 28, "bold"),
    text_color="white"
)
title.pack(side="left", padx=25, pady=20)

timeLabel = ctk.CTkLabel(
    header,
    text="",
    font=("Segoe UI",18,"bold"),
    text_color="white"
)

timeLabel.pack(side="right", padx=25)

# -----------------------------
# Left Frame
# -----------------------------
leftFrame = ctk.CTkFrame(
    app,
    width=420,
    corner_radius=20,
    fg_color="#1E293B", 
    border_width=2,
    border_color="#3B82F6"
)

leftFrame.pack(
    side="left",
    fill="y",
    padx=20,
    pady=(90,20)
)

# -----------------------------
# Right Frame
# -----------------------------
rightFrame = ctk.CTkFrame(
    app,
    corner_radius=20,
    fg_color="#0F172A",      # Dark Navy
    border_width=2,
    border_color="#3B82F6"
)

rightFrame.pack(
    side="right",
    expand=True,
    fill="both",
    padx=20,
    pady=(90,20)
)

# -----------------------------
# Logo
# -----------------------------
logo = ctk.CTkImage(
    light_image=Image.open("assets/logo.png"),
    dark_image=Image.open("assets/logo.png"),
    size=(180,180)
)

logoLabel = ctk.CTkLabel(
    leftFrame,
    image=logo,
    text=""
)
logoLabel.pack(pady=20)

# -----------------------------
# Title
# -----------------------------

# -----------------------------
# Camera Status
# -----------------------------
cameraStatus = ctk.CTkLabel(
    leftFrame,
    text="🟢 Camera Ready",
    font=("Arial",18)
)
cameraStatus.pack(pady=10)

# -----------------------------
# AI Status
# -----------------------------
aiStatus = ctk.CTkLabel(
    leftFrame,
    text="🟢 AI Ready",
    font=("Arial",18)
)
aiStatus.pack(pady=5)

cpuLabel = ctk.CTkLabel(
    leftFrame,
    text="💻 CPU : 0%",
    font=("Arial",16)
)

cpuLabel.pack(pady=5)

ramLabel = ctk.CTkLabel(
    leftFrame,
    text="🧠 RAM : 0%",
    font=("Arial",16)
)

ramLabel.pack(pady=5)

def blink():

    if "🟢" in cameraStatus.cget("text"):
        cameraStatus.configure(text="🟡 Camera Ready")
    else:
        cameraStatus.configure(text="🟢 Camera Ready")

    if aiStatus.cget("text") == "🟢 AI Ready":
        aiStatus.configure(text="🟢 Waiting for Module")
    else:
        aiStatus.configure(text="🟢 AI Ready")

    app.after(800, blink)

# -----------------------------
# Live Camera Preview
# -----------------------------
previewFrame = ctk.CTkFrame(leftFrame)

previewFrame.pack(pady=20)

previewLabel = ctk.CTkLabel(
    previewFrame,
    text=""
)

previewLabel.pack()

# -----------------------------
# Version
# -----------------------------
version = ctk.CTkLabel(
    leftFrame,
    text="Version 2.0",
    font=("Arial",15)
)
version.pack(side="bottom", pady=20)

# -----------------------------
# Heading
# -----------------------------
heading = ctk.CTkLabel(
    rightFrame,
    text="Select a Module",
    font=("Arial",30,"bold")
)
heading.pack(pady=30)
# -----------------------------
# Cards Container
# -----------------------------
cardsFrame = ctk.CTkFrame(
    rightFrame,
    fg_color="transparent"
)

cardsFrame.pack(pady=20)

row1 = ctk.CTkFrame(cardsFrame, fg_color="transparent")
row1.pack(pady=15)

mouseCard = ctk.CTkFrame(
    row1,
    width=200,
    height=140,
    corner_radius=20,
    fg_color="#1D4ED8"
)

mouseCard.pack(side="left", padx=15)

ctk.CTkLabel(
    mouseCard,
    text="🖱",
    font=("Segoe UI Emoji", 42)
).pack(pady=(15,5))

ctk.CTkLabel(
    mouseCard,
    text="Virtual Mouse",
    font=("Segoe UI",18,"bold")
).pack()

ctk.CTkButton(
    mouseCard,
    text="Open",
    width=120,
    command=launch_mouse
).pack(pady=15)

keyboardCard = ctk.CTkFrame(
    row1,
    width=200,
    height=140,
    corner_radius=20,
    fg_color="#2563EB"
)

keyboardCard.pack(side="left", padx=15)

ctk.CTkLabel(
    keyboardCard,
    text="⌨",
    font=("Segoe UI Emoji",42)
).pack(pady=(15,5))

ctk.CTkLabel(
    keyboardCard,
    text="Virtual Keyboard",
    font=("Segoe UI",18,"bold")
).pack()

ctk.CTkButton(
    keyboardCard,
    text="Open",
    width=120,
    command=launch_keyboard
).pack(pady=15)

row2 = ctk.CTkFrame(cardsFrame, fg_color="transparent")
row2.pack(pady=15)

gestureCard = ctk.CTkFrame(
    row2,
    width=200,
    height=140,
    corner_radius=20,
    fg_color="#3B82F6"
)

gestureCard.pack(side="left", padx=15)

ctk.CTkLabel(
    gestureCard,
    text="🚀",
    font=("Segoe UI Emoji",42)
).pack(pady=(15,5))

ctk.CTkLabel(
    gestureCard,
    text="Gesture Shortcuts",
    font=("Segoe UI",18,"bold")
).pack()

ctk.CTkButton(
    gestureCard,
    text="Open",
    width=120,
    command=launch_shortcuts
).pack(pady=15)

settingsCard = ctk.CTkFrame(
    row2,
    width=200,
    height=140,
    corner_radius=20,
    fg_color="#4F46E5"
)

settingsCard.pack(side="left", padx=15)

ctk.CTkLabel(
    settingsCard,
    text="⚙",
    font=("Segoe UI Emoji",42)
).pack(pady=(15,5))

ctk.CTkLabel(
    settingsCard,
    text="Settings",
    font=("Segoe UI",18,"bold")
).pack()

ctk.CTkButton(
    settingsCard,
    text="Open",
    width=120,
    command=lambda: subprocess.Popen([sys.executable,"settings.py"])
).pack(pady=15)


# -----------------------------
# Update Camera
# -----------------------------
def update_camera():

    global prevTime

    ret, frame = cap.read()

    if ret:

        currentTime = time.time()

        fps = int(1 / (currentTime - prevTime)) if currentTime != prevTime else 0

        prevTime = currentTime

        frame = cv2.flip(frame, 1)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        frame = cv2.resize(frame, (320,240))

        img = Image.fromarray(frame)

        photo = ImageTk.PhotoImage(img)

        previewLabel.configure(image=photo)

        previewLabel.image = photo

        fpsLabel.configure(text=f"FPS : {fps}")

    app.after(20, update_camera)

    

def update_time():

    now = datetime.now()

    timeLabel.configure(
        text=now.strftime("%d %b %Y   %I:%M:%S %p")
    )

    app.after(1000, update_time)

def system_status():

    cpu = psutil.cpu_percent()

    ram = psutil.virtual_memory().percent

    cpuLabel.configure(
        text=f"💻 CPU : {cpu}%"
    )

    ramLabel.configure(
        text=f"🧠 RAM : {ram}%"
    )

    app.after(1000, system_status)

# -----------------------------
# Footer
# -----------------------------
footer = ctk.CTkFrame(
    app,
    height=40,
    corner_radius=0,
    fg_color="#0B1120"
)

footer.place(
    relx=0,
    rely=1,
    relwidth=1,
    anchor="sw"
)
footerLeft = ctk.CTkLabel(
    footer,
    text="© 2026 AI Gesture Controller | Developed by SaranyaLam",
    font=("Segoe UI",13),
    text_color="white"
)

footerLeft.pack(
    side="left",
    padx=20
)
footerRight = ctk.CTkLabel(
    footer,
    text="Version 3.0   ✅ GitHub Ready",
    font=("Segoe UI",13,"bold"),
    text_color="#22C55E"
)

footerRight.pack(
    side="right",
    padx=20
)
fpsLabel = ctk.CTkLabel(
    footer,
    text="FPS : 0",
    font=("Segoe UI", 13),
    text_color="#38BDF8"
)

fpsLabel.pack(side="right", padx=180)

update_time()

system_status()

blink()

update_camera()
try:
    app.mainloop()
finally:
    cap.release()