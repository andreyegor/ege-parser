from time import sleep
import cv2
import numpy as np
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'Tesseract-OCR\tesseract.exe'

def solve(path, debug = False):
    # Grayscale, Gaussian blur, Otsu's threshold
    image = cv2.imread(path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3,3), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    invert = 255 - thresh

    # Perform text extraction
    data = pytesseract.image_to_string(invert, lang='eng',config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789').replace('\n','')
    
    if debug:
        print(data, len(data))
        cv2.imshow('thresh', thresh)
        cv2.imshow('invert', invert)
        cv2.waitKey()
        
    return data

if __name__ == '__main__':
    solve('captcha.png', debug=True)