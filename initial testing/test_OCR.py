import cv2
import pytesseract
import numpy as np

img = cv2.imread('./jimdoo.png')
gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
gray = cv2.bitwise_not(gray)

kernel = np.ones((2, 1), np.uint8)
img = cv2.erode(img, kernel, iterations=1)
img = cv2.dilate(img, kernel, iterations=1)
out_below = pytesseract.image_to_string(img)
print("OUTPUT:", out_below)