from PIL import Image
import numpy as np
from datetime import datetime
import cv2
import pytesseract
import time
from skimage.metrics import structural_similarity as ssim
import re
import easyocr

TESSERACT_PATH = r'C:\Program Files\Tesseract-OCR'
pytesseract.pytesseract_cmd = f"{TESSERACT_PATH}\\tesseract.exe"
SSIM_THRESHOLD = 0.95
MIN_TEXT_LENGTH = 50  # Minimum characters to consider valid extraction

class OCRProcessor:
    def __init__(self):
        self.previous_gray = None
        self.previous_text = ""
        self.previous_window = ""
        self.easyocr_reader = None
        self.content_type_cache = {}

    def preprocess_image(self, image, content_type):
        """Content-aware image preprocessing"""
        # Initial resize (balanced for speed/quality)
        image = cv2.resize(image, None, fx=1.3, fy=1.3, interpolation=cv2.INTER_CUBIC)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Content-specific processing
        if content_type == "code":
            if np.median(gray) < 127:  # Better dark mode detection
                gray = cv2.bitwise_not(gray)
            return cv2.adaptiveThreshold(
                gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY, 11, 2
            )
        elif content_type == "pdf":
            clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
            return clahe.apply(gray)
        elif content_type == "youtube":
            return cv2.threshold(
                cv2.GaussianBlur(gray, (3, 3), 0),
                255, 
                cv2.THRESH_BINARY | cv2.THRESH_OTSU
            )[1]
        else:  # General case
            return gray

    def clean_text(self, raw_text, content_type):
        """Comprehensive cleaning for all content types"""
        # Universal first-pass
        text = re.sub(r'[^\w\s\-.,:;!?\'"()\n\u2013\u2014]', '', raw_text)
        
        # Content-specific rules
        if content_type == "code":
            text = re.sub(r'(?<!\n)\n(?!\n)', ' ', text)  # Newlines → spaces
            text = re.sub(r'(def|class|import|from|return|if|else)([^\s])', r'\1 \2', text)
            text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)  # CamelCase
            
        elif content_type == "pdf":
            text = re.sub(r'(\w)-\s+(\w)', r'\1\2', text)  # Hyphen fix
            text = re.sub(r'Page\s*\d+\s*of\s*\d+', '', text)  # Page numbers
            
        elif content_type == "youtube":
            text = re.sub(r'\[.*?\]', '', text)  # [Music] tags
            text = re.sub(r'(?i)\b(subscribed|like|notification)\b', '', text)
            
        elif content_type == "email":
            text = re.sub(r'On\s.+\s(wrote|sent):.*$', '', text, flags=re.MULTILINE)
            text = re.sub(r'^>.*$', '', text, flags=re.MULTILINE)
            
        elif content_type == "webpage":
            text = re.sub(r'\b(Home|About|Contact)\b', '', text)
            text = re.sub(r'\d+\s*(comments|shares)', '', text)

        # Final cleanup
        text = re.sub(r'\s+', ' ', text).strip()
        return text[:3000]  # LLM length limit

    def detect_content_type(self, window_title):
        """Cached content detection with new types"""
        if window_title in self.content_type_cache:
            return self.content_type_cache[window_title]
            
        title_lower = window_title.lower()
        content_map = {
            "code": ["visual studio", "vscode", "pycharm", "intellij"],
            "pdf": ["pdf", "adobe", "foxit", "document"],
            "youtube": ["youtube", "netflix", "video"],
            "email": ["gmail", "outlook", "mail", "inbox"],
            "webpage": ["chrome", "edge", "firefox", "browser"],
            "doc": ["word", "powerpoint", "slides", "document"]
        }
        
        for content_type, keywords in content_map.items():
            if any(k in title_lower for k in keywords):
                self.content_type_cache[window_title] = content_type
                return content_type
                
        return "general"

    def extract_text(self, image, content_type):
        """Multi-engine text extraction"""
        preprocessed = self.preprocess_image(image, content_type)
        
        # Tesseract with optimized config
        config = '--oem 3 --psm 6'
        if content_type == "code":
            config += ' -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789{}[]()<>:;,.=+-*/\\\'"'
        tesseract_text = pytesseract.image_to_string(preprocessed, config=config)
        
        # Fallback to EasyOCR if poor results
        if len(tesseract_text.strip()) < MIN_TEXT_LENGTH/2:
            if self.easyocr_reader is None:
                self.easyocr_reader = easyocr.Reader(['en'], gpu=False)
            easyocr_text = ' '.join(self.easyocr_reader.readtext(
                preprocessed, paragraph=True, detail=0
            ))
            if len(easyocr_text) > len(tesseract_text):
                return self.clean_text(easyocr_text, content_type)
                
        return self.clean_text(tesseract_text, content_type)

    def process_frame(self, frame, window_title):
    
        if frame is None:
            print("Debug: Frame is None.")
            return None, None
    
        current_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        print("Debug: Current frame converted to grayscale.")
    
        # Skip if no significant change
        if (self.previous_gray is not None and 
            ssim(self.previous_gray, current_gray) > SSIM_THRESHOLD and
            window_title == self.previous_window):
            print("Debug: No significant changes detected. Skipping frame.")
            return None, current_gray
    
        content_type = self.detect_content_type(window_title)
        print(f"Debug: Detected content type: {content_type}")
    
        extracted_text = self.extract_text(frame, content_type)
        print(f"Debug: Extracted text length: {len(extracted_text)}")
    
        if len(extracted_text) < MIN_TEXT_LENGTH:
            print("Debug: Extracted text is too short. Skipping frame.")
            return None, current_gray
    
        # Update state
        self.previous_gray = current_gray
        self.previous_window = window_title
    
        return {
            "window_title": window_title,
            "content_type": content_type,
            "text": extracted_text,
            "timestamp": datetime.now().isoformat(),
            "is_code": content_type == "code",
            "is_media": content_type in ["youtube", "video"]
        }, current_gray