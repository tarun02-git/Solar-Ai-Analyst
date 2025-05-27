import numpy as np
import cv2
from PIL import Image
import io

def segment_rooftops(image: Image.Image):
    # Convert to grayscale
    img_np = np.array(image.convert('L'))
    # Apply adaptive thresholding to highlight rooftops
    thresh = cv2.adaptiveThreshold(img_np, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 51, 10)
    # Morphological operations to clean up
    kernel = np.ones((5,5), np.uint8)
    mask = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    return mask

def draw_rooftop_outlines(image: Image.Image, mask: np.ndarray):
    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    img_np = np.array(image.convert('RGB'))
    outlined = img_np.copy()
    cv2.drawContours(outlined, contours, -1, (0,255,0), 3)
    return Image.fromarray(outlined)

def mask_area(mask: np.ndarray, pixel_area_m2=0.25):
    # Assume each pixel is 0.5m x 0.5m (adjust for your imagery)
    return np.sum(mask > 0) * pixel_area_m2

def get_outlined_image_bytes(image: Image.Image, mask: np.ndarray):
    outlined = draw_rooftop_outlines(image, mask)
    buf = io.BytesIO()
    outlined.save(buf, format='PNG')
    buf.seek(0)
    return buf 