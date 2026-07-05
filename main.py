import subprocess
import sys
import os

while True:

    os.system("cls")

    print("=" * 40)
    print("     AI GESTURE CONTROLLER")
    print("=" * 40)
    print("1. Virtual Mouse")
    print("2. Gesture Shortcuts")
    print("3. Virtual Keyboard")
    print("4. Exit")
    print("=" * 40)

    choice = input("Enter your choice: ")

    if choice == "1":
        subprocess.run([sys.executable, "virtual_mouse.py"])

    elif choice == "2":
        subprocess.run([sys.executable, "gesture_shortcuts.py"])

    elif choice == "3":
        subprocess.run([sys.executable, "virtual_keyboard.py"])

    elif choice == "4":
        print("Thank you!")
        break

    else:
        input("Invalid choice! Press Enter...")