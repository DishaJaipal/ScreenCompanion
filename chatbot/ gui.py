import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
from PIL import Image, ImageTk
import random
import os 
import json
from chatbot import get_response_from_groq
from firebase_logger import log_to_firebase
from trigger_tray_popup import trigger_tray_popup
from productivity_logger import log_productivity
from app_controller.logic import launch_app_for_task
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent))  # Add project root to Python path
                      # Relative import
# === Load User Config === open("user_config.json") as f:

# Correct way to open and load a JSON file
with open("user_config.json") as f:
    user_info = json.load(f)  # Proper indentation inside the with block

# === Load Mascot Animations ===
mascot_animations = {
    "wave": ["mascot/wave1.png", "mascot/wave2.png", "mascot/wave3.png"],
    "nod": ["mascot/nod1.png", "mascot/nod2.png", "mascot/nod3.png"],
    "jump": ["mascot/jump1.png", "mascot/jump2.png", "mascot/jump3.png"]
}

# === Main GUI Window ===
root = tk.Tk()
root.title("ScreenAssistant IntelliBot")
root.geometry("800x850")
root.config(bg="#e0f7fa")

# === Mascot Area ===
mascot_label = tk.Label(root, bg="#e0f7fa")
mascot_label.pack(pady=10)
def get_response_from_groq(user_input):
    # Simple dummy responses
    responses = [
        "I'm a simple chatbot!",
        "Nice to meet you!",
        "What would you like to discuss?"
    ]
    return random.choice(responses)
def play_mascot_animation():
    action = random.choice(list(mascot_animations.keys()))
    for frame_path in mascot_animations[action]:
        img = Image.open(frame_path).resize((160, 160))
        photo = ImageTk.PhotoImage(img)
        mascot_label.config(image=photo)
        mascot_label.image = photo
        mascot_label.update()
        root.after(150)

# === Chat Display ===
chat_frame = tk.Frame(root, bg="white", bd=2, relief=tk.RIDGE)
chat_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

chat_log = tk.Text(chat_frame, height=25, width=80, bg="white", fg="black", font=("Arial", 12))
chat_log.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)
chat_log.config(state=tk.DISABLED)

def display_message(sender, message):
    chat_log.config(state=tk.NORMAL)
    chat_log.insert(tk.END, f"{sender}: {message}\n")
    chat_log.see(tk.END)
    chat_log.config(state=tk.DISABLED)

# === Input Section ===
entry_frame = tk.Frame(root, bg="#e0f7fa")
entry_frame.pack(pady=10)

entry = tk.Entry(entry_frame, width=60, font=("Arial", 12))
entry.pack(side=tk.LEFT, padx=10)

# === Core Interaction Functions ===
def send_message(msg=None):
    user_input = entry.get() if msg is None else msg
    if not user_input.strip():
        return
    entry.delete(0, tk.END)
    display_message("You", user_input)

    # Check focus mismatch
    if user_info["focus"].lower() not in user_input.lower():
        trigger_tray_popup()

    # Get Groq response
    response = get_response_from_groq(user_input)
    display_message("Bot", response)

    # Log to Firebase and local
    log_to_firebase(user_input, response)
    log_productivity(user_input)

    # Trigger mascot
    play_mascot_animation()

    # Check if task requires launching app
    if "open" in user_input.lower() or "start" in user_input.lower():
        keywords = ["note", "calculator", "browse", "doc"]
        for word in keywords:
            if word in user_input.lower():
                result = launch_app_for_task(f"write_{word}" if word != "calculator" else "calculate")
                display_message("System", result)

def listen_to_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        display_message("System", "🎙️ Listening...")
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Sorry, I didn't catch that."

def voice_message():
    user_input = listen_to_audio()
    display_message("You (via mic)", user_input)
    response = get_response_from_groq(user_input)
    display_message("Bot", response)
    log_to_firebase(user_input, response)
    log_productivity(user_input)
    play_mascot_animation()

# === Buttons ===
tk.Button(entry_frame, text="Send", font=("Arial", 12), command=send_message).pack(side=tk.LEFT)
tk.Button(entry_frame, text="🎙️ Speak", font=("Arial", 12), command=voice_message).pack(side=tk.LEFT, padx=5)

# === Start Message ===
# Safe way to access dictionary keys
welcome_message = "Welcome!"
if 'role' in user_info:
    welcome_message += f" {user_info['role']}!"
if 'focus' in user_info:
    welcome_message += f" Your focus today is '{user_info['focus']}'."

display_message("System", welcome_message)
root.mainloop()

