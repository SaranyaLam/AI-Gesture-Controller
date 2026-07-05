import customtkinter as ctk
from PIL import Image, ImageTk
import cv2
import subprocess
import sys

# -----------------------------
# Theme
# -----------------------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

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
cap = cv2.VideoCapture(0)

app.title("AI Gesture Controller")
app.geometry("1200x700")
app.resizable(False, False)

# -----------------------------
# Left Frame
# -----------------------------
leftFrame = ctk.CTkFrame(app, width=420, corner_radius=15)
leftFrame.pack(side="left", fill="y", padx=20, pady=20)

# -----------------------------
# Right Frame
# -----------------------------
rightFrame = ctk.CTkFrame(app, corner_radius=15)
rightFrame.pack(side="right", expand=True, fill="both", padx=20, pady=20)

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
title = ctk.CTkLabel(
    leftFrame,
    text="AI GESTURE\nCONTROLLER",
    font=("Arial",30,"bold")
)
title.pack(pady=10)

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

def blink():

    if aiStatus.cget("text") == "🟢 AI Ready":
        aiStatus.configure(text="🟢 Waiting for Module")
    else:
        aiStatus.configure(text="🟢 AI Ready")

    app.after(1000, blink)

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

stats = ctk.CTkFrame(rightFrame)
stats.pack(pady=15)

ctk.CTkLabel(
    stats,
    text="Modules : 3",
    font=("Arial",18)
).pack(pady=5)

ctk.CTkLabel(
    stats,
    text="Features : 10+",
    font=("Arial",18)
).pack(pady=5)

ctk.CTkLabel(
    stats,
    text="Python : 3.13",
    font=("Arial",18)
).pack(pady=5)

settingsBtn = ctk.CTkButton(
    rightFrame,
    text="⚙ Settings",
    width=350,
    height=60,
    command=lambda: subprocess.Popen([sys.executable, "settings.py"])
)

settingsBtn.pack(pady=20)

# -----------------------------
# Buttons (temporary)
# -----------------------------
mouseBtn = ctk.CTkButton(
    rightFrame,
    text="🖱 Virtual Mouse",
    width=350,
    height=60,
    command=launch_mouse
)
mouseBtn.pack(pady=20)

keyboardBtn = ctk.CTkButton(
    rightFrame,
    text="⌨ Virtual Keyboard",
    width=350,
    height=60,
    command=launch_keyboard
)
keyboardBtn.pack(pady=20)

shortcutBtn = ctk.CTkButton(
    rightFrame,
    text="🚀 Gesture Shortcuts",
    width=350,
    height=60,
    command=launch_shortcuts
)
shortcutBtn.pack(pady=20)

from tkinter import messagebox

def show_about():
    messagebox.showinfo(
        "About",
        "AI Gesture Controller\n\nBuilt with:\nPython\nOpenCV\nMediaPipe\nCustomTkinter"
    )

aboutBtn = ctk.CTkButton(
    rightFrame,
    text="ℹ About",
    width=350,
    height=60,
    command=show_about
)

aboutBtn.pack(pady=20)

exitBtn = ctk.CTkButton(
    rightFrame,
    text="❌ Exit",
    width=350,
    height=60,
    fg_color="red",
    hover_color="darkred",
    command=app.destroy
)
exitBtn.pack(pady=20)

# -----------------------------
# Update Camera
# -----------------------------
def update_camera():

    ret, frame = cap.read()

    if ret:

        frame = cv2.flip(frame, 1)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        frame = cv2.resize(frame, (320,240))

        img = Image.fromarray(frame)

        photo = ImageTk.PhotoImage(img)

        previewLabel.configure(image=photo)

        previewLabel.image = photo

    app.after(20, update_camera)

blink()

update_camera()
try:
    app.mainloop()
finally:
    cap.release()