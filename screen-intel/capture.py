from screen_pipe import capture_screen
from processor import extract_text_from_frame
from fluvio_sender import send_to_fluvio
from chatbot.firebase_logger import log_to_firebase
from chatbot.trigger_tray_popup import trigger_tray_popup
from chatbot.gui import play_mascot_animation
from shared_config import user_info

# Use `user_info["focus"]` in your logic

import time
import json
import os

# Load user focus config
with open("user_config.json") as f:
    user_info = json.load(f)

while True:
    frame = capture_screen()
    text = extract_text_from_frame(frame)

    if text:
        print(f"Extracted: {text}")
        send_to_fluvio(text)

        # Log to Firebase
        log_to_firebase("SCREEN_CAPTURE", text)

        # Focus check
        if user_info["focus"].lower() not in text.lower():
            trigger_tray_popup()

        # Mascot reaction
        play_mascot_animation()

    time.sleep(5)  # Capture every 5 seconds
