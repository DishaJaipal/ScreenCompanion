
# import tkinter as tk
# from tkinter import messagebox
# import speech_recognition as sr
# from PIL import Image, ImageTk
# import random
# import os
# import json
# import chatbot
# from chatbot import get_response_from_groq
# from firebase_logger import log_to_firebase
# from trigger_tray_popup import trigger_tray_popup
# from productivity_logger import log_productivity
# from app_controller.logic import launch_app_for_task
# from pathlib import Path
# import sys

# sys.path.append(str(Path(__file__).parent))

# # === Load User Config ===
# with open("user_config.json") as file:
#     user_info = json.load(file)

# # === Load Mascot Animations ===
# mascot_animations = {
#     "wave": ["mascot/wave1.png", "mascot/wave2.png", "mascot/wave3.png"],
#     "nod": ["mascot/nod1.png", "mascot/nod2.png", "mascot/nod3.png"],
#     "jump": ["mascot/jump1.png", "mascot/jump2.png", "mascot/jump3.png"]
# }

# # === Main GUI Window ===
# root = tk.Tk()
# root.title("ScreenAssistant IntelliBot")
# root.geometry("800x850")
# root.config(bg="#e0f7fa")

# # === Dynamic Top Frame for Role/Goal ===
# top_frame = tk.Frame(root, bg="#e0f7fa")

# def toggle_role_goal_visibility(event=None):
#     # Show fields only when window width >= 800px
#     if root.winfo_width() >= 800:
#         top_frame.pack(side=tk.TOP, fill=tk.X, pady=5)
#     else:
#         top_frame.pack_forget()

# # Role Input
# role_label = tk.Label(top_frame, text="Your Role:", bg="#e0f7fa", font=("Arial", 9))
# role_label.pack(side=tk.LEFT, padx=5)
# role_entry = tk.Entry(top_frame, width=20, font=("Arial", 9))
# role_entry.pack(side=tk.LEFT, padx=5)

# # Goal Input
# goal_label = tk.Label(top_frame, text="Your Goal:", bg="#e0f7fa", font=("Arial", 9))
# goal_label.pack(side=tk.LEFT, padx=5)
# goal_entry = tk.Entry(top_frame, width=20, font=("Arial", 9))
# goal_entry.pack(side=tk.LEFT, padx=5)

# # === Mascot Area ===
# mascot_label = tk.Label(root, bg="#e0f7fa")
# mascot_label.pack(pady=10)

# # === Chat Display ===
# chat_frame = tk.Frame(root, bg="white", bd=2, relief=tk.RIDGE)
# chat_frame.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

# chat_log = tk.Text(chat_frame, height=20, width=80, bg="white", fg="black", font=("Arial", 10))
# chat_log.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)
# chat_log.config(state=tk.DISABLED)

# def display_message(sender, message):
#     chat_log.config(state=tk.NORMAL)
#     chat_log.insert(tk.END, f"{sender}: {message}\n")
#     chat_log.see(tk.END)
#     chat_log.config(state=tk.DISABLED)

# # === Input Section ===
# entry_frame = tk.Frame(root, bg="#b2ebf2", bd=2, relief=tk.GROOVE)
# entry_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

# entry_label = tk.Label(entry_frame, text="🧠 Ask your assistant:", font=("Arial", 13, "bold"), bg="#b2ebf2")
# entry_label.pack(side=tk.TOP, anchor=tk.W)

# input_inner_frame = tk.Frame(entry_frame, bg="#b2ebf2")
# input_inner_frame.pack(padx=10, pady=(0, 10), fill=tk.X)

# entry = tk.Entry(input_inner_frame, width=40, font=("Arial", 12))
# entry.pack(side=tk.LEFT, padx=(0, 10), ipady=4, expand=True, fill=tk.X)

# send_button = tk.Button(input_inner_frame, text="Send", font=("Arial", 12), width=10, command=lambda: send_message())
# send_button.pack(side=tk.LEFT, padx=(0, 5))

# mic_button = tk.Button(input_inner_frame, text="🎙 Speak", font=("Arial", 12), width=10, command=lambda: voice_message())
# mic_button.pack(side=tk.LEFT)

# # === Core Functions ===
# def send_message(msg=None):
#     user_input = entry.get() if msg is None else msg
#     if not user_input.strip():
#         return
#     entry.delete(0, tk.END)
#     display_message("You", user_input)

#     if user_info["focus"].lower() not in user_input.lower():
#         trigger_tray_popup()

#     response = get_response_from_groq(user_input)
#     display_message("Bot", response)

#     log_to_firebase(user_input, response)
#     log_productivity(user_input)
#     play_mascot_animation()

#     if "open" in user_input.lower() or "start" in user_input.lower():
#         keywords = ["note", "calculator", "browse", "doc"]
#         for word in keywords:
#             if word in user_input.lower():
#                 task = f"write_{word}" if word != "calculator" else "calculate"
#                 result = launch_app_for_task(task)
#                 display_message("System", result)

# def listen_to_audio():
#     recognizer = sr.Recognizer()
#     with sr.Microphone() as source:
#         display_message("System", "🎙 Listening...")
#         audio = recognizer.listen(source)
#     try:
#         return recognizer.recognize_google(audio)
#     except sr.UnknownValueError:
#         return "Sorry, I didn't catch that."

# def voice_message():
#     user_input = listen_to_audio()
#     display_message("You (via mic)", user_input)
#     response = get_response_from_groq(user_input)
#     display_message("Bot", response)
#     log_to_firebase(user_input, response)
#     log_productivity(user_input)
#     play_mascot_animation()

# def play_mascot_animation():
#     action = random.choice(list(mascot_animations.keys()))
#     for frame_path in mascot_animations[action]:
#         img = Image.open(frame_path).resize((160, 160))
#         photo = ImageTk.PhotoImage(img)
#         mascot_label.config(image=photo)
#         mascot_label.image = photo
#         mascot_label.update()
#         root.after(150)

# # === Initial Setup ===
# root.bind("<Configure>", toggle_role_goal_visibility)
# toggle_role_goal_visibility()  # Initial check

# welcome_message = "Welcome!"
# if 'role' in user_info:
#     welcome_message += f" {user_info['role']}!"
# if 'focus' in user_info:
#     welcome_message += f" Your focus today is '{user_info['focus']}'."
# display_message("System", welcome_message)

# root.mainloop()


# import tkinter as tk
# from tkinter import messagebox
# import speech_recognition as sr
# from PIL import Image, ImageTk
# import random
# import os
# import json
# import threading
# import time
# import cv2
# from skimage.metrics import structural_similarity as ssim
# from pathlib import Path
# import sys
# from screen_capture import capture_screen, get_active_window_title
# from extracting import OCRProcessor
# from groq1 import generate_suggestion as get_response_from_groq
# from firebase_logger import log_to_firebase
# from trigger_tray_popup import trigger_tray_popup
# from productivity_logger import log_productivity
# from app_controller.logic import launch_app_for_task

# sys.path.append(str(Path(__file__).parent))

# # === Load User Config ===
# with open("user_config.json") as file:
#     user_info = json.load(file)

# # === Load Mascot Animations ===
# mascot_animations = {
#     "wave": ["mascot/wave1.png", "mascot/wave2.png", "mascot/wave3.png"],
#     "nod": ["mascot/nod1.png", "mascot/nod2.png", "mascot/nod3.png"],
#     "jump": ["mascot/jump1.png", "mascot/jump2.png", "mascot/jump3.png"]
# }

# class ScreenAssistant:
#     def _init_(self, root):
#         self.root = root
#         self.ocr = OCRProcessor()
#         self.running = False
#         self.last_update = 0
#         self.setup_gui()
        
#         # Initial window size check
#         self.toggle_role_goal_visibility()
        
#         # Start with welcome message
#         welcome_message = "Welcome!"
#         if 'role' in user_info:
#             welcome_message += f" {user_info['role']}!"
#         if 'focus' in user_info:
#             welcome_message += f" Your focus today is '{user_info['focus']}'."
#         self.display_message("System", welcome_message)

#     def setup_gui(self):
#         self.root.title("ScreenAssistant IntelliBot")
#         self.root.geometry("800x850")
#         self.root.config(bg="#e0f7fa")

#         # === Dynamic Top Frame for Role/Goal ===
#         self.top_frame = tk.Frame(self.root, bg="#e0f7fa")

#         # Role Input
#         self.role_label = tk.Label(self.top_frame, text="Your Role:", bg="#e0f7fa", font=("Arial", 9))
#         self.role_entry = tk.Entry(self.top_frame, width=20, font=("Arial", 9))
#         if "role" in user_info:
#             self.role_entry.insert(0, user_info["role"])

#         # Goal Input
#         self.goal_label = tk.Label(self.top_frame, text="Your Goal:", bg="#e0f7fa", font=("Arial", 9))
#         self.goal_entry = tk.Entry(self.top_frame, width=20, font=("Arial", 9))
#         if "focus" in user_info:
#             self.goal_entry.insert(0, user_info["focus"])

#         # === Mascot Area ===
#         self.mascot_label = tk.Label(self.root, bg="#e0f7fa")
#         self.mascot_label.pack(pady=10)

#         # === Chat Display ===
#         self.chat_frame = tk.Frame(self.root, bg="white", bd=2, relief=tk.RIDGE)
#         self.chat_frame.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

#         self.chat_log = tk.Text(self.chat_frame, height=20, width=80, bg="white", fg="black", font=("Arial", 10))
#         self.chat_log.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)
#         self.chat_log.config(state=tk.DISABLED)

#         # === Input Section ===
#         self.entry_frame = tk.Frame(self.root, bg="#b2ebf2", bd=2, relief=tk.GROOVE)
#         self.entry_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

#         entry_label = tk.Label(self.entry_frame, text="🧠 Ask your assistant:", font=("Arial", 13, "bold"), bg="#b2ebf2")
#         entry_label.pack(side=tk.TOP, anchor=tk.W)

#         input_inner_frame = tk.Frame(self.entry_frame, bg="#b2ebf2")
#         input_inner_frame.pack(padx=10, pady=(0, 10), fill=tk.X)

#         self.entry = tk.Entry(input_inner_frame, width=40, font=("Arial", 12))
#         self.entry.pack(side=tk.LEFT, padx=(0, 10), ipady=4, expand=True, fill=tk.X)
#         self.entry.bind("<Return>", lambda e: self.send_message())

#         self.monitor_btn = tk.Button(input_inner_frame, text="Start Monitoring", font=("Arial", 12), 
#                                     width=12, command=self.toggle_monitoring)
#         self.monitor_btn.pack(side=tk.LEFT, padx=(0, 5))

#         send_button = tk.Button(input_inner_frame, text="Send", font=("Arial", 12), width=10, 
#                                command=lambda: self.send_message())
#         send_button.pack(side=tk.LEFT, padx=(0, 5))

#         mic_button = tk.Button(input_inner_frame, text="🎙 Speak", font=("Arial", 12), width=10, 
#                               command=lambda: self.voice_message())
#         mic_button.pack(side=tk.LEFT)

#         # === Window Bindings ===
#         self.root.bind("<Configure>", self.toggle_role_goal_visibility)

#     def toggle_role_goal_visibility(self, event=None):
#         if self.root.winfo_width() >= 800:
#             self.role_label.pack(side=tk.LEFT, padx=5)
#             self.role_entry.pack(side=tk.LEFT, padx=5)
#             self.goal_label.pack(side=tk.LEFT, padx=5)
#             self.goal_entry.pack(side=tk.LEFT, padx=5)
#             self.top_frame.pack(side=tk.TOP, fill=tk.X, pady=5)
#         else:
#             self.top_frame.pack_forget()

#     # ===== SCREEN MONITORING ADDITIONS =====
#     def toggle_monitoring(self):
#         self.running = not self.running
#         self.monitor_btn.config(text="Stop Monitoring" if self.running else "Start Monitoring")
        
#         if self.running:
#             threading.Thread(target=self.monitor_loop, daemon=True).start()
#             self.display_message("System", "Screen monitoring started (5-minute intervals)")
#         else:
#             self.display_message("System", "Screen monitoring stopped")

#     def monitor_loop(self):
#         while self.running:
#             try:
#                 if time.time() - self.last_update >= 300:  # 5 minutes
#                     frame = capture_screen()
#                     window = get_active_window_title()
                    
#                     if frame is not None and window:
#                         result, _ = self.ocr.process_frame(frame, window)
#                         if result and result.get("text"):
#                             self.process_screen_change(result, window)
#                             self.last_update = time.time()
                
#                 time.sleep(10)  # Check every 10 seconds
#             except Exception as e:
#                 self.display_message("System", f"Monitoring error: {str(e)}")
#                 time.sleep(30)

#     def process_screen_change(self, result, window):
#         role = self.role_entry.get().strip()
#         goal = self.goal_entry.get().strip()
        
#         if not role or not goal:
#             self.display_message("System", "Please set role and goal first!")
#             return
            
#         try:
#             response = get_response_from_groq(role, goal, result["text"], window)
#             self.display_message("Assistant", f"Screen changed to {window}:\n{response}")
            
#             # Log to Firebase
#             log_to_firebase({
#                 "event": "screen_change",
#                 "window": window,
#                 "response": response
#             })
            
#         except Exception as e:
#             self.display_message("System", f"API Error: {str(e)}")

#     # ===== ORIGINAL CHATBOT FUNCTIONS (UNCHANGED) =====
#     def send_message(self, msg=None):
#         user_input = self.entry.get() if msg is None else msg
#         if not user_input.strip():
#             return

#         self.entry.delete(0, tk.END)
#         self.display_message("You", user_input)

#         if user_info["focus"].lower() not in user_input.lower():
#             trigger_tray_popup()

#         try:
#             response = get_response_from_groq(
#                 self.role_entry.get().strip(),
#                 self.goal_entry.get().strip(),
#                 None,
#                 "User Input"
#             )
#             self.display_message("Assistant", response)
            
#             log_to_firebase(user_input, response)
#             log_productivity(user_input)
#             self.play_mascot_animation()

#             if "open" in user_input.lower() or "start" in user_input.lower():
#                 keywords = ["note", "calculator", "browse", "doc"]
#                 for word in keywords:
#                     if word in user_input.lower():
#                         task = f"write_{word}" if word != "calculator" else "calculate"
#                         result = launch_app_for_task(task)
#                         self.display_message("System", result)

#         except Exception as e:
#             self.display_message("System", f"Error: {str(e)}")

#     def voice_message(self):
#         try:
#             recognizer = sr.Recognizer()
#             with sr.Microphone() as source:
#                 self.display_message("System", "🎙 Listening...")
#                 audio = recognizer.listen(source)
                
#             user_input = recognizer.recognize_google(audio)
#             self.display_message("You (via mic)", user_input)
#             self.send_message(user_input)
            
#         except sr.UnknownValueError:
#             self.display_message("System", "Sorry, I didn't catch that.")
#         except Exception as e:
#             self.display_message("System", f"Voice error: {str(e)}")

#     def play_mascot_animation(self):
#         action = random.choice(list(mascot_animations.keys()))
#         for frame_path in mascot_animations[action]:
#             try:
#                 img = Image.open(frame_path).resize((160, 160))
#                 photo = ImageTk.PhotoImage(img)
#                 self.mascot_label.config(image=photo)
#                 self.mascot_label.image = photo
#                 self.mascot_label.update()
#                 self.root.after(150)
#             except:
#                 continue

#     def display_message(self, sender, message):
#         self.chat_log.config(state=tk.NORMAL)
#         self.chat_log.insert(tk.END, f"{sender}: {message}\n")
#         self.chat_log.see(tk.END)
#         self.chat_log.config(state=tk.DISABLED)

#     def on_close(self):
#         """Save config when closing"""
#         with open("user_config.json", "w") as f:
#             json.dump({
#                 "role": self.role_entry.get(),
#                 "focus": self.goal_entry.get()
#             }, f)
#         self.root.destroy()

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = ScreenAssistant(root)
#     root.protocol("WM_DELETE_WINDOW", app.on_close)
#     root.mainloop()

import tkinter as tk
from tkinter import messagebox
import json
import threading
import time
from PIL import Image, ImageTk
from screen_capture import capture_screen, get_active_window_title
from extracting import OCRProcessor
from groq1 import generate_suggestion
from firebase_logger import log_to_firebase
from chatbot import get_response_from_groq
from voice_input import listen_to_audio

class ScreenAssistant:
    def __init__(self, root):
        self.root = root
        self.ocr_processor = OCRProcessor()
        self.running = False
        self.last_update = 0
        self.setup_gui()
        self.load_config()
        self.setup_bindings()

    def setup_gui(self):
        self.root.title("Productivity Companion")
        self.root.geometry("800x750")
        self.root.config(bg="#e0f7fa")

        # Top Section - Role/Goal
        self.top_frame = tk.Frame(self.root, bg="#e0f7fa")
        
        self.role_label = tk.Label(
            self.top_frame, 
            text="Role:", 
            bg="#e0f7fa", 
            font=("Arial", 9)
        )
        self.role_entry = tk.Entry(
            self.top_frame, 
            width=24, 
            font=("Arial", 9)
        )
        self.goal_label = tk.Label(
            self.top_frame, 
            text="Goal:", 
            bg="#e0f7fa", 
            font=("Arial", 9)
        )
        self.goal_entry = tk.Entry(
            self.top_frame, 
            width=24, 
            font=("Arial", 9)
        )

        self.role_label.pack(side=tk.LEFT, padx=2)
        self.role_entry.pack(side=tk.LEFT, padx=2)
        self.goal_label.pack(side=tk.LEFT, padx=2)
        self.goal_entry.pack(side=tk.LEFT, padx=2)
        self.top_frame.pack(pady=2)

        # Chat Display Area
        self.chat_frame = tk.Frame(self.root, bg="white")
        self.chat_log = tk.Text(
            self.chat_frame,
            height=22,
            width=85,
            font=("Arial", 10),
            bg="white",
            fg="black",
            wrap=tk.WORD
        )
        self.chat_log.pack(padx=5, pady=2, fill=tk.BOTH, expand=True)
        self.chat_frame.pack(padx=5, pady=2, fill=tk.BOTH, expand=True)
        self.chat_log.config(state=tk.DISABLED)

        # Input Section
        self.input_frame = tk.Frame(self.root, bg="#b2ebf2")
        
        self.entry = tk.Entry(
            self.input_frame,
            font=("Arial", 11),
            width=38
        )
        self.entry.pack(side=tk.LEFT, padx=2)
        
        self.voice_btn = tk.Button(
            self.input_frame,
            text="🎙",
            command=self.voice_message,
            width=4
        )
        self.voice_btn.pack(side=tk.LEFT, padx=2)
        
        self.send_btn = tk.Button(
            self.input_frame,
            text="Send",
            command=self.send_message,
            width=6
        )
        self.send_btn.pack(side=tk.LEFT, padx=2)
        
        self.monitor_btn = tk.Button(
            self.input_frame,
            text="Start Monitoring",
            command=self.toggle_monitoring,
            width=12
        )
        self.monitor_btn.pack(side=tk.LEFT, padx=2)
        
        self.input_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=3)

    def setup_bindings(self):
        self.root.bind("<Configure>", self.toggle_role_goal_visibility)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def toggle_role_goal_visibility(self, event=None):
        if self.root.winfo_width() >= 700:
            self.top_frame.pack(pady=2)
        else:
            self.top_frame.pack_forget()

    def toggle_monitoring(self):
        self.running = not self.running
        new_text = "Stop Monitoring" if self.running else "Start Monitoring"
        self.monitor_btn.config(text=new_text)
        
        if self.running:
            monitor_thread = threading.Thread(target=self.monitor_loop)
            monitor_thread.daemon = True
            monitor_thread.start()

    def monitor_loop(self):
     while self.running:
        try:
            if time.time() - self.last_update >= 10:
                frame = capture_screen()
                window_title = get_active_window_title()  # Get window title here
                
                if frame is not None:
                    result = self.ocr_processor.process_frame(frame, window_title)
                    
                    if isinstance(result, tuple):
                        processed_data, _ = result
                        if processed_data and processed_data.get('text'):
                            # FIX: Pass window_title as the 4th argument
                            suggestion = generate_suggestion(
                                self.role_entry.get(),
                                self.goal_entry.get(),
                                processed_data['text'],
                                window_title  # <-- THIS WAS MISSING
                            )
                            self.display_message("Analysis", suggestion)
                            log_to_firebase(processed_data['text'], suggestion)
                            self.last_update = time.time()
            time.sleep(10)
        except Exception as e:
            self.display_message("Error", f"Monitoring: {str(e)}")
    def send_message(self):
        user_input = self.entry.get().strip()
        if not user_input:
            return
        
        self.display_message("You", user_input)
        try:
            response = get_response_from_groq(user_input)
            self.display_message("Assistant", response)
            log_to_firebase(user_input, response)
            self.entry.delete(0, tk.END)
        except Exception as e:
            self.display_message("Error", f"API Error: {str(e)}")

    def voice_message(self):
        try:
            self.display_message("System", "🎤 Listening...")
            text = listen_to_audio()
            if text:
                self.entry.delete(0, tk.END)
                self.entry.insert(0, text)
                self.display_message("You (Voice)", text)
        except Exception as e:
            self.display_message("Error", f"Voice Error: {str(e)}")

    def display_message(self, sender, message):
        self.chat_log.config(state=tk.NORMAL)
        self.chat_log.insert(tk.END, f"{sender}: {message}\n")
        self.chat_log.see(tk.END)
        self.chat_log.config(state=tk.DISABLED)

    def load_config(self):
        try:
            with open("user_config.json", "r") as config_file:
                config_data = json.load(config_file)
                self.role_entry.insert(0, config_data.get("role", ""))
                self.goal_entry.insert(0, config_data.get("goal", ""))
        except FileNotFoundError:
            self.display_message("System", "No config file found")
        except json.JSONDecodeError:
            self.display_message("System", "Invalid config file format")

    def save_config(self):
        config_data = {
            "role": self.role_entry.get().strip(),
            "goal": self.goal_entry.get().strip()
        }
        with open("user_config.json", "w") as config_file:
            json.dump(config_data, config_file, indent=2)

    def on_close(self):
        self.save_config()
        self.running = False
        self.root.destroy()
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenAssistant(root)
    root.mainloop()