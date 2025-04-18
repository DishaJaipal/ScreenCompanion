import mss
import cv2
import numpy as np

def capture_screen():
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # Full screen
        img = sct.grab(monitor)
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
        return frame
