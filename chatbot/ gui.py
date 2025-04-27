import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
from PIL import Image, ImageTk
import random
import os 
import json
from pathlib import Path
import sys
import chatbot 
from chatbot import get_response_from_groq  # Ensure this import is correct
from firebase_logger import log_to_firebase
from trigger_tray_popup import trigger_tray_popup
from productivity_logger import log_productivity
from app_controller.logic import launch_app_for_task

BASE_DIR = Path(__file__).parent.parent
sys.path.append(str(BASE_DIR))

try:
    with open(BASE_DIR / "user_config.json") as f:
        user_info = json.load(f)
except FileNotFoundError:
    messagebox.showerror("Error", "Missing user_config.json")
    sys.exit(1)
except json.JSONDecodeError:
    messagebox.showerror("Error", "Invalid user_config.json")
    sys.exit(1)

# === Fixed Mascot Path Handling ===
MASCOT_DIR = BASE_DIR / "mascot"
mascot_animations = {
    "wave": [MASCOT_DIR / "wave1.png", MASCOT_DIR / "wave2.png", MASCOT_DIR / "wave3.png"],
    "nod": [MASCOT_DIR / "nod1.png", MASCOT_DIR / "nod2.png", MASCOT_DIR / "nod3.png"],
    "jump": [MASCOT_DIR / "jump1.png", MASCOT_DIR / "jump2.png", MASCOT_DIR / "jump3.png"]
}

# === Main GUI Window ===
root = tk.Tk()
root.title("ScreenAssistant IntelliBot")
root.geometry("800x850")
root.config(bg="#e0f7fa")

# === Fixed Mascot Animation Function ===
def play_mascot_animation():
    try:
        action = random.choice(list(mascot_animations.keys()))
        for frame_path in mascot_animations[action]:
            if not frame_path.exists():
                continue
            img = Image.open(frame_path).resize((160, 160))
            photo = ImageTk.PhotoImage(img)
            mascot_label.config(image=photo)
            mascot_label.image = photo
            root.update_idletasks()
            root.after(150)
    except Exception as e:
        print(f"Animation error: {str(e)}")

def listen_to_audio():
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            display_message("System", "🎙️ Listening...")
            audio = recognizer.listen(source, timeout=5)
        return recognizer.recognize_google(audio)
    except sr.WaitTimeoutError:
        return "No speech detected"
    except Exception as e:
        print(f"Audio error: {str(e)}")
        return "Audio input failed"

# === Fixed Focus Check ===
def check_focus_mismatch(user_input):
    focus = user_info.get("focus", "").lower()
    if focus and (focus not in user_input.lower()):
        trigger_tray_popup()

# === Fixed Welcome Message ===
def show_welcome_message():
    welcome = "Welcome!"
    if user_info.get('role'):
        welcome += f" {user_info['role']}!"
    if user_info.get('focus'):
        welcome += f"\nYour focus today is: '{user_info['focus']}'"
    display_message("System", welcome)

# === Fixed Application Launch ===
def handle_app_launch(user_input):
    if "open" in user_input.lower() or "start" in user_input.lower():
        tasks = {
            "note": "write_note",
            "calculator": "calculate",
            "browse": "browser",
            "doc": "document"
        }
        for word, task in tasks.items():
            if word in user_input.lower():
                result = launch_app_for_task(task)
                display_message("System", result)
                return

# === Updated Send Message Function ===
def send_message(msg=None):
    user_input = entry.get() if msg is None else msg
    if not user_input.strip():
        return
    
    entry.delete(0, tk.END)
    display_message("You", user_input)
    
    # Check focus mismatch
    check_focus_mismatch(user_input)
    
    try:
        response = get_response_from_groq(user_input)
        display_message("Bot", response)
        log_to_firebase(user_input, response)
        log_productivity(user_input)
        handle_app_launch(user_input)
    except Exception as e:
        display_message("System", f"Error: {str(e)}")
    
    play_mascot_animation()

# ... (rest of the GUI setup code remains the same)

# Initialize welcome message
show_welcome_message()
root.mainloop()