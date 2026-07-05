import customtkinter as ctk
from PIL import Image
import subprocess
import sys

# -----------------------------
# Theme
# -----------------------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# -----------------------------
# Window
# -----------------------------
app = ctk.CTk()
app.geometry("650x450")
app.title("AI Gesture Controller")
app.resizable(False, False)

app.configure(fg_color="#08121F")

# Center Window
screen_w = app.winfo_screenwidth()
screen_h = app.winfo_screenheight()

x = (screen_w - 650) // 2
y = (screen_h - 450) // 2

app.geometry(f"650x450+{x}+{y}")

# -----------------------------
# Main Frame
# -----------------------------
mainFrame = ctk.CTkFrame(
    app,
    corner_radius=20,
    fg_color="#0F172A",
    border_width=2,
    border_color="#2563EB"
)

mainFrame.pack(fill="both", expand=True, padx=20, pady=20)

# -----------------------------
# Logo
# -----------------------------
logo = ctk.CTkImage(
    light_image=Image.open("assets/logo.png"),
    dark_image=Image.open("assets/logo.png"),
    size=(140,140)
)

logoLabel = ctk.CTkLabel(
    mainFrame,
    image=logo,
    text=""
)

logoLabel.pack(pady=(25,10))

# -----------------------------
# Title
# -----------------------------
title = ctk.CTkLabel(
    mainFrame,
    text="🤖 AI GESTURE CONTROLLER",
    font=("Segoe UI",28,"bold"),
    text_color="#60A5FA"
)

title.pack()

# -----------------------------
# Version
# -----------------------------
version = ctk.CTkLabel(
    mainFrame,
    text="Version 3.0",
    font=("Segoe UI",16),
    text_color="white"
)

version.pack()

# -----------------------------
# Status
# -----------------------------
status = ctk.CTkLabel(
    mainFrame,
    text="Initializing...",
    font=("Segoe UI",18)
)

status.pack(pady=20)

# -----------------------------
# Progress
# -----------------------------
progress = ctk.CTkProgressBar(
    mainFrame,
    width=500,
    height=18,
    progress_color="#2563EB"
)

progress.pack()

progress.set(0)

# -----------------------------
# Percentage
# -----------------------------
percent = ctk.CTkLabel(
    mainFrame,
    text="0%",
    font=("Segoe UI",18,"bold")
)

percent.pack(pady=10)

# -----------------------------
# Footer
# -----------------------------
footer = ctk.CTkLabel(
    mainFrame,
    text="© 2026 AI Gesture Controller",
    font=("Segoe UI",13),
    text_color="gray"
)

footer.pack(side="bottom", pady=20)

# -----------------------------
# Loading Animation
# -----------------------------
value = 0

messages = [
    "Initializing AI...",
    "Loading OpenCV...",
    "Loading MediaPipe...",
    "Preparing Camera...",
    "Starting Launcher..."
]

def loading():
    global value

    value += 1

    progress.set(value/100)

    percent.configure(text=f"{value}%")

    if value < 20:
        status.configure(text=messages[0])

    elif value < 40:
        status.configure(text=messages[1])

    elif value < 60:
        status.configure(text=messages[2])

    elif value < 80:
        status.configure(text=messages[3])

    else:
        status.configure(text=messages[4])

    if value < 100:
        app.after(35, loading)
    else:
        app.destroy()
        subprocess.Popen([sys.executable, "launcher.py"])

loading()

app.mainloop()