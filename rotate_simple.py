import cv2
import pytesseract
from os import walk
from utils import *
3,4
3,6
3,11

3,4,opening
#3,11,gray
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

dir_path = './cards/'

img = cv2.imread('./test_cards/Trygon.jpg')

scale_percent = 30 # percent of original size
width = int(img.shape[1] * scale_percent / 100)
height = int(img.shape[0] * scale_percent / 100)
dim = (width, height)

img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)


gray = get_grayscale(img)
thresh = thresholding(gray)
opening = opening(gray)
canny = canny(gray)

#print(gray)
custom_config = r'--oem 3 --psm 4'

text = pytesseract.image_to_string(opening, config=custom_config)
print(text)

input()

from pytesseract import Output
import pytesseract
import argparse
import imutils
import cv2
from utils import opening
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
custom_config = r'--oem 3 --psm 4'

image = cv2.imread('./test_cards/Trygon.jpg')
image = cv2.resize(image, (907, 1209))

#cv2.imshow(image)

rgb = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
img = opening(rgb)
text = pytesseract.image_to_string(img, config=custom_config)
print(text)
#cv2.imwrite('output.jpg', rgb)
results = pytesseract.image_to_osd(rgb, config=custom_config, output_type=Output.DICT)

rotated = imutils.rotate_bound(image, angle=results["rotate"])
#cv2.imshow(image)
#cv2.imshow(rotated)
#cv2.waitKey(0)