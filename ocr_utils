# OCR 모듈 함수들입니다.

import pytesseract
import os
from PIL import ImageGrab, Image

# Tesseract 경로 지정
pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

# 이미지 저장 경로 생성
save_dir = "이미지 파일"
os.makedirs(save_dir, exist_ok=True)

def get_save_dir():
    return save_dir

def capture_and_ocr(region, filename):
    img_path = os.path.join(save_dir, filename)
    screenshot = ImageGrab.grab(bbox=region)
    screenshot.save(img_path, format="PNG")
    image_file = Image.open(img_path)
    return pytesseract.image_to_string(image_file, config='--psm 11 --oem 3')
