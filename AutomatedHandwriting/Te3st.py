import os

import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
import numpy as np
from PIL import Image, ImageFilter

rgba_Character = Image.open("C:/Users/wwwku/source/repos/AutomatedHandwriting/HorizontalCrop1.png")
rgb_Character=rgba_Character.convert("RGB")
CharacterImage = np.array(rgb_Character)
Character = pytesseract.image_to_string(CharacterImage)
print(Character)