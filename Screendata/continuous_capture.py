import os 
from skimage.metrics import structural_similarity as ssim
import cv2
import numpy as np
import groq
from Screendata.screen_capture import get_active_window_title ,capture_screen
from extracting import process_screenshot
from groq1 import 




def calculate_ssim(img1, img2):
    """Calculate Structural Similarity Index (SSIM) between two images."""
    score, _ = ssim(img1, img2, full=True)
    return score