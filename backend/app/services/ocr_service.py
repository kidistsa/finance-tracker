# import pytesseract
# from PIL import Image
# import re
# import io
# from datetime import datetime
# from typing import Dict, Any, Optional, List
# import logging

# logger = logging.getLogger(__name__)

# # Set Tesseract path for Windows
# import platform
# if platform.system() == 'Windows':
#     pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# class OCRService:
#     # Common patterns for receipt extraction
#     DATE_PATTERNS = [
#         r"(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})",
#         r"(\d{4}[/-]\d{1,2}[/-]\d{1,2})",
#         r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2},?\s+\d{4}",
#     ]
    
#     AMOUNT_PATTERNS = [
#         r"TOTAL[:\s]*\$?(\d+\.\d{2})",
#         r"AMOUNT[:\s]*\$?(\d+\.\d{2})",
#         r"DUE[:\s]*\$?(\d+\.\d{2})",
#         r"PAYMENT[:\s]*\$?(\d+\.\d{2})",
#         r"\$(\d+\.\d{2})\s*$",
#         r"(\d+\.\d{2})\s*$",
#     ]
    
#     @staticmethod
#     async def extract_from_image(image_file) -> Dict[str, Any]:
#         try:
#             image = Image.open(io.BytesIO(await image_file.read()))
#             image = OCRService._preprocess_image(image)
#             text = pytesseract.image_to_string(image)
#             logger.info(f"OCR extracted text: {text[:200]}...")
#             receipt_data = OCRService._parse_receipt_text(text)
#             return receipt_data
#         except Exception as e:
#             logger.error(f"OCR extraction failed: {e}")
#             return {"error": str(e)}
    
#     @staticmethod
#     def _preprocess_image(image):
#         if image.mode != 'L':
#             image = image.convert('L')
        
#         import numpy as np
#         import cv2
        
#         img_array = np.array(image)
#         _, img_array = cv2.threshold(img_array, 150, 255, cv2.THRESH_BINARY)
#         return Image.fromarray(img_array)
    
#     @staticmethod
#     def _parse_receipt_text(text: str) -> Dict[str, Any]:
#         result = {
#             "merchant": None,
#             "date": None,
#             "total": None,
#             "items": [],
#             "raw_text": text
#         }
        
#         lines = text.strip().split('\n')
#         if lines:
#             for line in lines[:5]:
#                 line = line.strip()
#                 if line and len(line) > 3 and not OCRService._is_amount(line) and not OCRService._is_date(line):
#                     result["merchant"] = line
#                     break
        
#         for pattern in OCRService.DATE_PATTERNS:
#             match = re.search(pattern, text, re.IGNORECASE)
#             if match:
#                 date_str = match.group(1)
#                 result["date"] = OCRService._parse_date(date_str)
#                 break
        
#         for pattern in OCRService.AMOUNT_PATTERNS:
#             match = re.search(pattern, text, re.IGNORECASE)
#             if match:
#                 result["total"] = float(match.group(1))
#                 break
        
#         lines = text.split('\n')
#         for line in lines:
#             price_match = re.search(r'(\d+\.\d{2})$', line)
#             if price_match:
#                 item = {
#                     "description": line[:line.rfind(price_match.group(1))].strip(),
#                     "amount": float(price_match.group(1))
#                 }
#                 if item["description"] and len(item["description"]) > 2:
#                     result["items"].append(item)
        
#         return result
    
#     @staticmethod
#     def _is_amount(text: str) -> bool:
#         return bool(re.search(r'^\$?\d+\.\d{2}$', text.strip()))
    
#     @staticmethod
#     def _is_date(text: str) -> bool:
#         for pattern in OCRService.DATE_PATTERNS:
#             if re.match(pattern, text.strip(), re.IGNORECASE):
#                 return True
#         return False
    
#     @staticmethod
#     def _parse_date(date_str: str) -> Optional[str]:
#         try:
#             for fmt in ['%m/%d/%Y', '%m-%d-%Y', '%Y-%m-%d', '%m/%d/%y']:
#                 try:
#                     date = datetime.strptime(date_str, fmt)
#                     return date.strftime('%Y-%m-%d')
#                 except ValueError:
#                     continue
            
#             from dateutil import parser
#             date = parser.parse(date_str)
#             return date.strftime('%Y-%m-%d')
#         except:
#             return datetime.now().strftime('%Y-%m-%d')
