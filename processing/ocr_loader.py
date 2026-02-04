import pytesseract
from PIL import Image
from processing.text_to_json import text_to_json

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def load_image_ocr(image_path):
    try:
        img = Image.open(image_path).convert("L")
        text = pytesseract.image_to_string(img, config="--oem 3 --psm 6")

        if text and text.strip():
            return text_to_json(text.strip(), source="ocr")

        return None
    except Exception as e:
        print("OCR Error:", e)
        return None
