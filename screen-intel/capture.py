from screen_pipe import capture_screen
from processor import extract_text_from_frame
from fluvio_sender import send_to_fluvio
import time

while True:
    frame = capture_screen()
    text = extract_text_from_frame(frame)

    if text:
        print(f"Extracted: {text}")
        send_to_fluvio(text)
    
    time.sleep(5)  # Capture every 5 sec
