import os
from skimage.metrics import structural_similarity as ssim
import cv2
import numpy as np
import groq
from screen_capture import get_active_window_title, capture_screen
from extracting import process_screenshot
from groq1 import generate_suggestion
import time
import pyautogui
import easyocr
import pygetwindow as gw

def calculate_ssim(img1, img2):
    """Calculate Structural Similarity Index (SSIM) between two images."""
    score, _ = ssim(img1, img2, full=True)
    return score

def main():  # Main function for execution logic
    previous_gray = None
    while True:
        # Get active window title
        try:
            active_window = gw.getActiveWindow()
            window_title = active_window.title if active_window else "Unknown Window"
        except Exception as e:
            print(f"Error getting active window: {e}")
            window_title = "Unknown Window"

        # Capture screenshot
        current_frame = capture_screen()

        if current_frame is None:
            print("Error: Failed to capture screen.")
             # Wait and retry
            continue

        # Process the screenshot
        result, previous_gray = process_screenshot(current_frame, previous_gray, window_title)

        if result:
            print(f"Window Title: {result['window_title']}")
            print(f"Extracted Text: {result['text']}")
            generate_suggestion(
                role="student",
                goal="studying for my operating system program",
                text=result['text'],
                window=result['window_title']
            )

        time.sleep(300)  # 5 minutes interval

