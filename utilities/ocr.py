import cv2
from PIL import Image
import pytesseract
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'



def extract_image_data(image_path):
    try:
        # Load the image using OpenCV
        img_cv = cv2.imread(image_path)

        if img_cv is None:
            print(f"Error: Could not open or find the image at {image_path}")
            return ""

        # Convert to grayscale
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)

        # Apply Otsu's thresholding for binarization
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Convert OpenCV image (NumPy array) to PIL Image for pytesseract
        img_pil = Image.fromarray(thresh)

        # Use pytesseract to extract text
        text = pytesseract.image_to_string(img_pil, lang='ron')
        print(text.strip())

        return text.strip()

    except pytesseract.TesseractNotFoundError:
        print("Error: Tesseract is not installed or not found in your PATH.")
        print("Please install Tesseract OCR engine and ensure it's accessible.")
        print("If on Windows, you might need to specify 'tesseract_cmd_path'.")
        return ""
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""