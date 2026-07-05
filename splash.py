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
# Splash Window
# -----------------------------
app = ctk.CTk()
app.geometry("600x400")
app.title("Loading...")
app.resizable(False, False)

# Center the window
screen_w = app.winfo_screenwidth()
screen_h = app.winfo_screenheight()

x = (screen_w - 600) // 2
y = (screen_h - 400) // 2

app.geometry(f"600x400+{x}+{y}")

# -----------------------------
# Logo
# -----------------------------
logo = ctk.CTkImage(
    light_image=Image.open("assets/logo.png"),
    dark_image=Image.open("assets/logo.png"),
    size=(120,120)
)

logoLabel = ctk.CTkLabel(app, image=logo, text="")
logoLabel.pack(pady=20)

# -----------------------------
# Title
# -----------------------------
title = ctk.CTkLabel(
    app,
    text="AI GESTURE CONTROLLER",
    font=("Arial",24,"bold")
)
title.pack()

status = ctk.CTkLabel(
    app,
    text="Loading AI Modules...",
    font=("Arial",16)
)
status.pack(pady=15)

# -----------------------------
# Progress Bar
# -----------------------------
progress = ctk.CTkProgressBar(app, width=450)
progress.pack(pady=20)
progress.set(0)

value = 0

def loading():
    global value

    value += 0.02
    progress.set(value)

    if value < 1:
        app.after(60, loading)
    else:
        app.destroy()
        subprocess.Popen([sys.executable, "launcher.py"])

loading()

app.mainloop()