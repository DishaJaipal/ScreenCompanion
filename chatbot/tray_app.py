# tray_app.py
import pystray
from pystray import MenuItem as item
from PIL import Image
import threading
import os
import sys
import tkinter as tk
from tkinter import messagebox

# Load a small mascot icon (you can use any PNG)
def create_image():
    icon_path = "mascot/wave1.png"  # Use one of your mascot icons
    return Image.open(icon_path).resize((64, 64))

# Actions from the tray
def on_open():
    os.system(f"{sys.executable} gui.py")  # Reopen chatbot window

def on_exit():
    tray_icon.stop()
    os._exit(0)

def on_about():
    tk.Tk().withdraw()
    messagebox.showinfo("About", "IntelliBot Desktop Assistant\nWith Tray & Firebase")

# Set up the tray icon
tray_icon = pystray.Icon("IntelliBot")
tray_icon.icon = create_image()
tray_icon.title = "IntelliBot"
tray_icon.menu = pystray.Menu(
    item("Open Assistant", on_open),
    item("About", on_about),
    item("Exit", on_exit)
)

def run_tray():
    tray_icon.run()