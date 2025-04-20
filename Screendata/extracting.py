# from PIL import Image
# import numpy as np
# from datetime import datetime
# from screen_capture import capture_screen, get_active_window_title
# import pygetwindow as gw
# import pyautogui
# import cv2
# import pytesseract
# import time
# from skimage.metrics import structural_similarity as ssim
# import re

# # --- CONFIG ---
# CAPTURE_INTERVAL = 10
#   # every 300 seconds
# SSIM_THRESHOLD = 0.95  

# # Specify the path to Tesseract
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# # --- ENHANCED FUNCTIONS ---
# def calculate_ssim(img1, img2):
#     """Calculate structural similarity between two images"""
#     score, _ = ssim(img1, img2, full=True)
#     return score

# def enhanced_preprocess(image):
#     """Improved preprocessing pipeline for better OCR results"""
#     # Convert to grayscale
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
#     # Contrast enhancement
#     clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
#     enhanced = clahe.apply(gray)
    
#     # Adaptive thresholding
#     thresh = cv2.adaptiveThreshold(enhanced, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#                                  cv2.THRESH_BINARY, 11, 2)
    
#     # Denoising
#     denoised = cv2.fastNlMeansDenoising(thresh, h=10, templateWindowSize=7, searchWindowSize=21)
    
#     # Morphological operations
#     kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
#     cleaned = cv2.morphologyEx(denoised, cv2.MORPH_CLOSE, kernel)
    
#     # Save for debugging
#     cv2.imwrite("debug_preprocessed.png", cleaned)
    
#     return cleaned

# def clean_extracted_text(text):
#     """Advanced text cleaning with multiple filters"""
#     # Remove non-ASCII characters
#     text = ''.join(char for char in text if ord(char) < 128)
    
#     # Common OCR error patterns
#     corrections = [
#         (r'[|]', 'I'),  # Common OCR error for 'I'
#         (r'[}{]', 'I'),  # Common OCR error for 'I'
#         (r'[)(]', 'I'),  # Common OCR error for 'I'
#         (r'\b[a-zA-Z]\b', ''),  # Remove single letters
#         (r'\b[0-9]+\b', ''),    # Remove standalone numbers
#         (r'[^\w\s\'-]', ' '),   # Keep only letters, numbers, and basic punctuation
#         (r'\s+', ' '),          # Normalize whitespace
#     ]
    
#     for pattern, replacement in corrections:
#         text = re.sub(pattern, replacement, text)
    
#     # Remove lines with mostly garbage
#     lines = []
#     for line in text.split('\n'):
#         words = line.split()
#         if len(words) >= 2 or any(len(word) > 3 for word in words):
#             lines.append(' '.join(words))
    
#     return '\n'.join(lines).strip()

# def extract_text_from_image(image):
#     """Enhanced text extraction with better preprocessing"""
#     try:
#         # Preprocess the image
#         preprocessed = enhanced_preprocess(image)
        
#         # Save preprocessed image for debugging
#         # cv2.imwrite("debug_preprocessed.png", preprocessed)
        
#         # Perform OCR with optimized settings
#         custom_config = r'--oem 3 --psm 6 -l eng'
#         text = pytesseract.image_to_string(preprocessed, config=custom_config)
        
    
        
#         # Clean the extracted text
#         cleaned_text = clean_extracted_text(text)
        
#         return cleaned_text if cleaned_text else ""
#     except Exception as e:
#         print(f"Error during OCR: {e}")
#         return ""

# # --- MAIN LOOP (UNCHANGED STRUCTURE) ---
# previous_gray = None
# f_text = ""

# while True:
#     try:
#         result = capture_screen()
#         current_frame = result["frame"]
#         current_gray = result["gray_frame"]
#         current_window = result["window_title"]

#         if previous_gray is not None:
#             similarity = calculate_ssim(previous_gray, current_gray)
            
#             if similarity < SSIM_THRESHOLD:
#                 text = extract_text_from_image(current_frame)
#                 if text:  # Only update if we got meaningful text
#                     f_text = text[:700]  # Limit to 700 characters
                
#                 # Print structured output
#                 print("\n" + "="*50)
#                 print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
#                 print(f"Window: {current_window}")
#                 print("-"*50)
#                 print("Extracted Text:")
#                 print(f_text)
#                 print("="*50 + "\n")

#         # Store current image for next comparison
#         previous_gray = current_gray.copy()
#         time.sleep(CAPTURE_INTERVAL)
        
#     except Exception as e:
#         print(f"Error in main loop: {e}")
#         time.sleep(5)  # Wait before trying again
from PIL import Image
import numpy as np
from datetime import datetime
from screen_capture import capture_screen, get_active_window_title
import cv2
import pytesseract
import time
from skimage.metrics import structural_similarity as ssim
import re
import os

# --- CONFIG ---
CAPTURE_INTERVAL = 10  # seconds
SSIM_THRESHOLD = 0.95
MIN_WORD_LENGTH = 4
MIN_LINE_LENGTH = 3

# Tesseract Configuration
TESSERACT_PATH = r'C:\Program Files\Tesseract-OCR'
pytesseract.pytesseract.tesseract_cmd = os.path.join(TESSERACT_PATH, 'tesseract.exe')
os.environ['TESSDATA_PREFIX'] = os.path.join(TESSERACT_PATH, 'tessdata')

def calculate_ssim(img1, img2):
    """Calculate structural similarity between two images"""
    score, _ = ssim(img1, img2, full=True)
    return score

# ---=APPLICATION-SPECIFIC PROFILES ---
def preprocess_vscode(image):
    """Optimized for VS Code's dark theme and monospace font"""
    # Invert dark theme
    inverted = cv2.bitwise_not(image)
    # Enhance contrast
    lab = cv2.cvtColor(inverted, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    cl = clahe.apply(l)
    processed = cv2.merge((cl,a,b))
    return cv2.cvtColor(processed, cv2.COLOR_LAB2BGR)

def preprocess_whatsapp(image):
    """Optimized for WhatsApp's green theme and message bubbles"""
    # Crop to message area (adjust coordinates as needed)
    roi = image[100:-50, 50:-50]
    # Enhance text in bubbles
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    return thresh

def preprocess_gmail(image):
    """Optimized for Gmail's interface"""
    # Focus on email content area
    roi = image[150:-100, 50:-50]
    # Standard preprocessing
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    return cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                              cv2.THRESH_BINARY, 11, 2)

def preprocess_pdf(image):
    """Optimized for PDF viewers"""
    # Sharpening filter
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    sharpened = cv2.filter2D(image, -1, kernel)
    # Contrast enhancement
    lab = cv2.cvtColor(sharpened, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    processed = cv2.merge((clahe.apply(l), a, b))
    return cv2.cvtColor(processed, cv2.COLOR_LAB2BGR)

# --- TEXT PROCESSING ---
def clean_general_text(text):
    """Basic cleaning for most applications"""
    text = re.sub(r'[^\w\s\'-]', ' ', text)  # Keep basic punctuation
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def clean_code_text(text):
    """Special cleaning for code"""
    # Fix common OCR errors in code
    replacements = {
        'O': '0', 'I': '1', 'Z': '2', 
        'S': '5', 'B': '8', 'tt': 't',
        'aa': 'a', 'mm': 'm', 'cv2': 'cv2.'
    }
    for wrong, right in replacements.items():
        text = text.replace(wrong, right)
    return text

def filter_valid_content(text, is_code=False):
    """Remove gibberish lines"""
    lines = []
    for line in text.split('\n'):
        words = [word for word in line.split() 
                if len(word) >= MIN_WORD_LENGTH or is_code]
        if len(words) >= (1 if is_code else MIN_LINE_LENGTH):
            lines.append(' '.join(words))
    return '\n'.join(lines)

# --- CORE FUNCTIONS ---
def get_ocr_config(window_title):
    """Return application-specific OCR configuration"""
    if "Visual Studio Code" in window_title:
        return r'--oem 3 --psm 11 -c tessedit_char_blacklist=}{[]|\\'  # Code mode
    elif "WhatsApp" in window_title:
        return r'--oem 3 --psm 4'  # Single column
    elif "Gmail" in window_title:
        return r'--oem 3 --psm 3'  # Block of text
    elif "Adobe" in window_title or "PDF" in window_title:
        return r'--oem 3 --psm 6'  # Assume uniform text
    else:
        return r'--oem 3 --psm 6'  # Default

def preprocess_image(image, window_title):
    """Application-specific preprocessing"""
    if "Visual Studio Code" in window_title:
        return preprocess_vscode(image)
    elif "WhatsApp" in window_title:
        return preprocess_whatsapp(image)
    elif "Gmail" in window_title:
        return preprocess_gmail(image)
    elif "Adobe" in window_title or "PDF" in window_title:
        return preprocess_pdf(image)
    else:
        # Default preprocessing
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY, 11, 2)

def extract_text(image, window_title):
    """Main text extraction pipeline"""
    try:
        processed = preprocess_image(image, window_title)
        config = get_ocr_config(window_title)
        
        text = pytesseract.image_to_string(processed, config=config)
        
        # Application-specific cleaning
        if "Visual Studio Code" in window_title:
            text = clean_code_text(text)
            text = filter_valid_content(text, is_code=True)
        else:
            text = clean_general_text(text)
            text = filter_valid_content(text)
            
        return text.strip()
    except Exception as e:
        print(f"OCR Error: {str(e)[:100]}")
        return ""

# --- MAIN LOOP ---
previous_gray = None

try:
    while True:
        result = capture_screen()
        current_frame = result["frame"]
        current_gray = result["gray_frame"]
        current_window = result["window_title"]

        if previous_gray is not None:
            similarity = calculate_ssim(previous_gray, current_gray)
            
            if similarity < SSIM_THRESHOLD:
                text = extract_text(current_frame, current_window)
                if text:
                    print("\n" + "="*50)
                    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                    print(f"Window: {current_window}")
                    print("-"*50)
                    print("Extracted Text:")
                    print(text[:1000])  # Limit to 1000 chars
                    print("="*50)

        previous_gray = current_gray.copy()
        time.sleep(CAPTURE_INTERVAL)

except KeyboardInterrupt:
    print("\nMonitoring stopped by user.")