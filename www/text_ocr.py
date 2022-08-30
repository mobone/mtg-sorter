import cv2
import pytesseract
from os import walk
from utils import *

from fuzzywuzzy import fuzz
import sqlite3
import os
import pandas as pd
import time



conn = sqlite3.connect('card.db')
df = pd.read_sql('select name from cards_unique', conn)

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

img = cv2.imread('./static/current_scan.jpg')

    
dim = (img.shape[1], img.shape[0])
top_img = img[0:300, 0:dim[0]]
bottom_img = img[dim[1]-150:dim[1], 0:dim[0]]

#cv2.imwrite('./static/cropped.jpg', img)

scale_percent = 150 # percent of original size
width = int(img.shape[1] * scale_percent / 100)
height = int(img.shape[0] * scale_percent / 100)
dim = (width, height)

top_img_scaled = cv2.resize(top_img, dim, interpolation = cv2.INTER_AREA)
bottom_img_scaled = cv2.resize(bottom_img, dim, interpolation = cv2.INTER_AREA)

#gray_img = get_grayscale(img)
top_img_scaled = get_grayscale(top_img_scaled)
bottom_img_scaled = get_grayscale(bottom_img_scaled)
#opening_img = opening(gray_img)

#gray_img_scaled = get_grayscale(img_scaled)
#opening_img_scaled = opening(gray_img_scaled)

custom_config = r'--oem 3 --psm 4'

text_top = pytesseract.image_to_string(top_img_scaled, config=custom_config)
text_bottom = pytesseract.image_to_string(bottom_img_scaled, config=custom_config)
#text_original_scaled = pytesseract.image_to_string(opening_img_scaled, config=custom_config)
#text_gray_img_scaled = pytesseract.image_to_string(gray_img_scaled, config=custom_config)

print(text_top)
print(text_bottom)
exit()

max_score = 0
best_text = None
best_text_type = None
best_text = None

for text, text_type in [(text_gray_img, 'gray'), (text_gray_img_scaled, 'gray_scaled')]:
#for text, text_type in [(text_gray_img, 'gray')]:
    print(">", text, text_type)
    if text is None or text == '':
        continue
    print('----------------')
    print(text)
    print('----------------')
    #input()
    for key, row in df.iterrows():

        ratio = fuzz.ratio(text, row.values[0])
        if ratio<50:
            continue
        if ratio > max_score:
            best_text = row.values[0]
            best_text_type = text_type
            max_score = ratio
            print(ratio, '\t', best_text_type, '\t', best_text)

