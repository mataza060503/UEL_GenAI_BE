from pdf2image import convert_from_path
import pytesseract
from PIL import Image, ImageOps, ImageFilter
import os

class PDFService:

    @staticmethod
    def preprocess_image(image: Image) -> Image:
        """
        Preprocess the image to improve OCR accuracy.
        - Convert to grayscale.
        - Apply thresholding to create a binary image.
        - Optionally apply denoising and other filters.
        """
        # Convert to grayscale
        image = image.convert("L")
        
        # Apply thresholding (binarization)
        image = image.point(lambda p: p > 180 and 255)  # Simple threshold

        # Optionally apply denoising using a filter (e.g., median filter)
        image = image.filter(ImageFilter.MedianFilter(3))  # Denoising

        # Optionally invert image (useful in some cases where black text is on white background)
        image = ImageOps.invert(image)

        # You can also resize the image to improve OCR results
        image = image.resize((image.width * 2, image.height * 2), Image.LANCZOS)  # Double the size

        return image

    @staticmethod
    def extract_text_with_ocr(pdf_path, page_number):
        """
        Extract text from a PDF file using OCR if the text is not extractable via pdfplumber.
        Converts PDF pages to images, applies preprocessing, and uses pytesseract for OCR.
        """
        try:
            pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
            # Convert the specified page of the PDF to an image
            images = convert_from_path(pdf_path, first_page=page_number, last_page=page_number, poppler_path=r'C:\Program Files\poppler-24.08.0\Library\bin')

            if not images:
                raise ValueError(f"No images found for page {page_number}.")

            # Process the image (preprocess for better OCR)
            image = images[0]  # Since we are processing only one page at a time
            processed_image = PDFService.preprocess_image(image)

            # Extract text from the processed image using pytesseract
            text = pytesseract.image_to_string(processed_image)

            return text
        except Exception as e:
            print(f"Error during OCR extraction from {pdf_path} on page {page_number}: {e}")
            return None
