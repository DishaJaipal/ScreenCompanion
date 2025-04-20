import threading
import subprocess
import os
import time
from datetime import datetime
from screen_pipe import get_active_window_title, capture_screen
from chatbot.chatbot import get_groq_suggestion
from utils.logger import log_event

def run_gui():
    subprocess.run(["python", os.path.join("chatbot", "gui.py")])

def run_capture():
    subprocess.run(["python", os.path.join("screen-intel", "capture.py")])

def run_screen_assistant():
    previous_window = ""
    print("[👁️ ScreenAssistant] Monitoring tab switches...")

    try:
        while True:
            current_window = get_active_window_title()
            if current_window != previous_window and current_window.strip() != "":
                print(f"\n[🔀] Switched to: {current_window}")

                event_data = {
                    "event": "window_switch",
                    "window_title": current_window,
                    "timestamp": datetime.now().isoformat()
                }
                log_event(event_data)

                capture_screen()  # Optional
                suggestion = get_groq_suggestion(current_window)
                print(f"[🤖 Suggestion] {suggestion}")

                previous_window = current_window
            time.sleep(2)
    except KeyboardInterrupt:
        print("[🛑] ScreenAssistant stopped.")

# Launch all components in parallel
threading.Thread(target=run_gui).start()
threading.Thread(target=run_capture).start()
threading.Thread(target=run_screen_assistant).start()
