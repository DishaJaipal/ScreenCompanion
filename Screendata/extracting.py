from PIL import Image
import numpy as np
from datetime import datetime
from screen_capture import capture_screen, get_active_window_title
import pygetwindow as gw
import pyautogui
import cv2
import pytesseract
import time
from skimage.metrics import structural_similarity as ssim
import re

import easyocr
import numpy as np



# TESSERACT_PATH = r'C:\Program Files\Tesseract-OCR'
# pytesseract.pytesseract_cmd = f"{TESSERACT_PATH}\\tesseract.exe"
# SSIM_THRESHOLD = 0.95  # Threshold for detecting changes in screenshots

# # --- FUNCTIONS ---
# def calculate_ssim(img1, img2):
#      score, _ = ssim(img1, img2, full=True)
#      return score
# def preprocess_image(image, content_type):
#     """Preprocess images based on the content type."""
#     image = cv2.resize(image, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC)

#     if content_type in ["code", "pdf", "webpage"]:
#         inverted = cv2.bitwise_not(image)  # Handle dark themes
#         gray = cv2.cvtColor(inverted, cv2.COLOR_BGR2GRAY)
#         clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))  # Contrast enhancement
#         enhanced = clahe.apply(gray)
#         _, thresholded = cv2.threshold(enhanced, 127, 255, cv2.THRESH_BINARY)
#         return thresholded

#     elif content_type in ["whatsapp", "gmail", "youtube"]:
#         gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#         blurred = cv2.GaussianBlur(gray, (5, 5), 0)
#         thresholded = cv2.adaptiveThreshold(
#             blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
#         )
#         return thresholded

#     else:
#         return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Default preprocessing

# def clean_text(raw_text):
#     """Clean extracted text for readability."""
#     text = re.sub(r'[^\w\s\'\-.:,]', '', raw_text)
#     text = re.sub(r'\s+', ' ', text).strip()
#     return text

# def detect_content_type(window_title):
#     """Infer content type from the window title."""
#     if "Visual Studio Code" in window_title or "Code" in window_title:
#         return "code"
#     elif ".pdf" in window_title or "Adobe" in window_title:
#         return "pdf"
#     elif "Chrome" in window_title or "Edge" in window_title or "Firefox" in window_title:
#         return "webpage"
#     elif "WhatsApp" in window_title:
#         return "whatsapp"
#     elif "Gmail" in window_title or "Inbox" in window_title:
#         return "gmail"
#     elif "YouTube" in window_title:
#         return "youtube"
#     else:
#         return "general"

# def process_screenshot(screenshot, previous_gray):
#     """Extract text from a screenshot and return it for Groq."""
#     current_frame = screenshot["frame"]
#     current_gray = screenshot["gray_frame"]
#     window_title = screenshot["window_title"]

#     content_type = detect_content_type(window_title)

#     if previous_gray is None or calculate_ssim(previous_gray, current_gray) < SSIM_THRESHOLD:
#         preprocessed_image = preprocess_image(current_frame, content_type)
#         if content_type in ["code", "pdf", "webpage"]:
#             extracted_text = clean_text(pytesseract.image_to_string(preprocessed_image, config='--oem 3 --psm 6'))
#         else:
#             reader = easyocr.Reader(['en'], gpu=False)
#             extracted_text = clean_text(' '.join(reader.readtext(preprocessed_image, detail=0)))

#         if extracted_text:
#             return {"text": extracted_text, "window_title": window_title}, current_gray

#     return None, current_gray




# --- CONFIGURATION ---
TESSERACT_PATH = r'C:\Program Files\Tesseract-OCR'
pytesseract.pytesseract_cmd = f"{TESSERACT_PATH}\\tesseract.exe"
SSIM_THRESHOLD = 0.95  # Threshold for detecting changes in screenshots

# --- FUNCTIONS ---
def preprocess_image(image, content_type):
    """Preprocess images based on the content type."""
    image = cv2.resize(image, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC)

    if content_type in ["code", "pdf", "webpage"]:
        inverted = cv2.bitwise_not(image)  # Handle dark themes
        gray = cv2.cvtColor(inverted, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))  # Contrast enhancement
        enhanced = clahe.apply(gray)
        _, thresholded = cv2.threshold(enhanced, 127, 255, cv2.THRESH_BINARY)
        return thresholded

    elif content_type in ["whatsapp", "gmail", "youtube"]:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        thresholded = cv2.adaptiveThreshold(
            blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
        return thresholded

    else:
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Default preprocessing

def clean_text(raw_text):
    """Clean extracted text for readability."""
    text = re.sub(r'[^\w\s\'\-.:,]', '', raw_text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def detect_content_type(window_title):
    """Infer content type from the window title."""
    if "Visual Studio Code" in window_title or "Code" in window_title:
        return "code"
    elif ".pdf" in window_title or "Adobe" in window_title:
        return "pdf"
    elif "Chrome" in window_title or "Edge" in window_title or "Firefox" in window_title:
        return "webpage"
    elif "WhatsApp" in window_title:
        return "whatsapp"
    elif "Gmail" in window_title or "Inbox" in window_title:
        return "gmail"
    elif "YouTube" in window_title:
        return "youtube"
    else:
        return "general"

def process_screenshot(current_frame, previous_gray, window_title):
    """Extract text from the current frame if it's different from the previous one."""
    # Convert current frame to grayscale for comparison
    current_gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)

    # Check if the frame has changed (based on SSIM)
    if previous_gray is None or calculate_ssim(previous_gray, current_gray) < SSIM_THRESHOLD:
        # Detect content type from window title
        content_type = detect_content_type(window_title)

        # Preprocess the current frame
        preprocessed_image = preprocess_image(current_frame, content_type)

        # Extract text based on content type
        if content_type in ["code", "pdf", "webpage"]:
            extracted_text = clean_text(pytesseract.image_to_string(preprocessed_image, config='--oem 3 --psm 6'))
        else:
            reader = easyocr.Reader(['en'], gpu=False)
            extracted_text = clean_text(' '.join(reader.readtext(preprocessed_image, detail=0)))

        # Return the extracted text and update the previous_gray frame
        if extracted_text:
            return {"text": extracted_text, "window_title": window_title}, current_gray

    # If the frame hasn't changed, return None
    return None, previous_gray
