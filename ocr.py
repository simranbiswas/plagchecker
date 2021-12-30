import os
import cv2
import pytesseract

def ocr_text(filename):
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    img = cv2.imread(os.path.join("static/uploads", filename))
    img = cv2.resize(img, None, fx=0.5, fy=0.5)    # scaling
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)   # grayscale
    # binarization
    adaptive_threshold = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 85, 21)

    config = "--psm 4"    # full page segmentation (0 - 10)
    t = pytesseract.image_to_string(gray)
    text = pytesseract.image_to_string(adaptive_threshold, config=config)

    return text

