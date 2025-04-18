import tkinter as tk
from firebase_logger import log_to_firebase
from trigger_tray_popup import trigger_tray_popup
from shared_config import user_info

from tkinter import messagebox
import speech_recognition as sr
import random
from PIL import Image, ImageTk
import os

# === Load Mascot Animations ===
mascot_animations = {
    "wave": ["mascot/wave1.png", "mascot/wave2.png", "mascot/wave3.png"],
    "nod": ["mascot/nod1.png", "mascot/nod2.png", "mascot/nod3.png"],
    "jump": ["mascot/jump1.png", "mascot/jump2.png", "mascot/jump3.png"]
}

# === Main GUI Window ===
root = tk.Tk()
root.title("IntelliBot")
root.geometry("720x800")
root.config(bg="#e0f7fa")

mascot_label = tk.Label(root, bg="#e0f7fa")
mascot_label.pack(pady=5)

def play_mascot_animation():
    action = random.choice(list(mascot_animations.keys()))
    frames = mascot_animations[action]
    for frame_path in frames:
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
    chat_log.insert(tk.END, f"\n{sender}: {message}\n")
    chat_log.see(tk.END)
    chat_log.config(state=tk.DISABLED)

def dummy_response(msg):
    # Dummy logic, replace with real model integration
    return f"I'm thinking about: {msg}!"

# === Input Section ===
entry_frame = tk.Frame(root, bg="#e0f7fa")
entry_frame.pack(pady=10)

entry = tk.Entry(entry_frame, width=60, font=("Arial", 12))
entry.pack(side=tk.LEFT, padx=10)

def send_message(msg=None):
    user_input = entry.get() if msg is None else msg
    if not user_input.strip():
        return
    entry.delete(0, tk.END)
    display_message("You", user_input)

    response = dummy_response(user_input)
    display_message("Bot", response)

    log_to_firebase(user_input, response) 
    play_mascot_animation()

    if user_info["focus"] and user_info["focus"].lower() not in user_input.lower():
        trigger_tray_popup()

def listen_to_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
    try:
        return r.recognize_google(audio)
    except sr.UnknownValueError:
        return "Sorry, I didn't catch that."

def voice_message():
    user_input = listen_to_audio()
    display_message("You (via Mic)", user_input)
    response = dummy_response(user_input)
    display_message("Bot", response)
    log_to_firebase(user_input, response)
    play_mascot_animation()

    if user_info["focus"] and user_info["focus"].lower() not in user_input.lower():
        trigger_tray_popup()

tk.Button(entry_frame, text="Send", font=("Arial", 12), command=send_message).pack(side=tk.LEFT)
tk.Button(entry_frame, text="🎙️ Speak", font=("Arial", 12), command=voice_message).pack(side=tk.LEFT, padx=5)

# === Ask Role/Focus Modal ===
def ask_user_info():
    def submit():
        user_info["role"] = role_var.get()
        user_info["focus"] = focus_entry.get()
        display_message("System", f"Hello {user_info['role']}! Today's focus: {user_info['focus']}")
        info_win.destroy()

    info_win = tk.Toplevel(root)
    info_win.title("Welcome to IntelliBot")
    info_win.geometry("400x250")
    info_win.grab_set()

    tk.Label(info_win, text="Select your role:", font=("Arial", 12)).pack(pady=5)
    role_var = tk.StringVar(value="Student")
    tk.OptionMenu(info_win, role_var, "Student", "Developer", "Researcher", "Other").pack()

    tk.Label(info_win, text="What's your main focus today?", font=("Arial", 12)).pack(pady=10)
    focus_entry = tk.Entry(info_win, width=40)
    focus_entry.pack(pady=5)

    tk.Button(info_win, text="Start Chatting", font=("Arial", 12), command=submit).pack(pady=15)

ask_user_info()
root.mainloop()
