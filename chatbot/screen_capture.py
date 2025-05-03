import pygetwindow as gw
import pyautogui
import numpy as np
import cv2

def get_active_window_title():
    try:
        win = gw.getActiveWindow()
        if win:
            return win.title
    except:
        return "Unknown Window"
    return "No Active Window"

def capture_screen():
    try:
        screenshot = pyautogui.screenshot()
        frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        return frame
    except Exception as e:
        print(f"Error capturing screen: {e}")
        return None

#result=capture_screen()
#print(result["window_title"])
# Display the captured frame
#cv2.imshow("Screen Capture", result["frame"])

# Wait for 10 seconds (10,000 milliseconds)
#cv2.waitKey(10000)

# Close the window
#cv2.destroyAllWindows()

# from PIL import Images
# import numpy as np
# from datetime import datetime
# from screen_capture import capture_screen  , get_active_window_title,convert_to_grayscale
# import pygetwindow as gw
# import pyautogui
# import numpy as np
# import cv2
# import pytesseract
# import time

# # --- CONFIG ---
# CAPTURE_INTERVAL = 300  # every 5 mins = 300 seconds
# SSIM_THRESHOLD = 0.95   # similarity threshold

# # --- FUNCTIONS ---



# def calculate_ssim(img1, img2):
#     from skimage.metrics import structural_similarity as ssim
#     score, _ = ssim(img1, img2, full=True)
#     return score

# def extract_text_from_image(image):
#     text = pytesseract.image_to_string(image)
#     return text

# # --- MAIN LOOP ---
# previous_gray = None
# previous_capture = None

# while True:
#     result = capture_screen()
#     current_frame = result["frame"]
#     current_gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
#     print(f"[{time.ctime()}] Captured from: {result['window_title']}")

#     if previous_gray is not None:
#         similarity = calculate_ssim(previous_gray, current_gray)
#         print(f"Similarity: {similarity:.4f}")

#         if similarity < SSIM_THRESHOLD:
#             print("🧠 Screen content changed — running OCR...")
#             text = extract_text_from_image(current_frame)
#             print("Extracted Text:\n", text.strip()[:500] or "[No readable text]")
#         else:
#             print("✅ Screen unchanged. Skipping OCR.")

#     # Store current image for next comparison
#     previous_gray = current_gray.copy()
#     previous_capture = current_frame.copy()

#     print("⏳ Waiting 5 mins...\n")
#     time.sleep(CAPTURE_INTERVAL)
