import os
import cv2
import pytesseract
from google.cloud import vision

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"indigo-bazaar-345413-1cb88e1db7e8.json"


def CloudVisionTextExtractor(handwritings):
    # convert image from numpy to bytes for submittion to Google Cloud Vision
    _, encoded_image = cv2.imencode('.png', handwritings)
    content = encoded_image.tobytes()
    image = vision.Image(content=content)

    # feed handwriting image segment to the Google Cloud Vision API
    client = vision.ImageAnnotatorClient()
    response = client.document_text_detection(image=image)

    return response


def getTextFromVisionResponse(response):
    texts = []
    for page in response.full_text_annotation.pages:
        for i, block in enumerate(page.blocks):
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    word_text = ''.join([symbol.text for symbol in word.symbols])
                    texts.append(word_text)

    return ' '.join(texts)


def ocr_text(filename):
    # pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    img = cv2.imread(os.path.join("static/uploads", filename))
    img = cv2.resize(img, None, fx=0.5, fy=0.5)  # scaling
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # grayscale
    adaptive_threshold = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 85, 21)

    # config = "--psm 4"  # full page segmentation (0 - 10)
    # text = pytesseract.image_to_string(adaptive_threshold, config=config)
    img_text = adaptive_threshold
    response = CloudVisionTextExtractor(img_text)
    text = getTextFromVisionResponse(response)
    print(text)

    return text
