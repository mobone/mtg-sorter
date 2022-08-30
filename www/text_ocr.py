import cv2
import pytesseract
from os import walk
from utils import *

from fuzzywuzzy import fuzz
import sqlite3
import os
import pandas as pd
import time
from pytesseract import Output
import pytesseract
import argparse
import imutils
import cv2
from PIL import Image 

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

print(pytesseract.image_to_osd(Image.open('./static/test.jpg'))) 


image = cv2.imread('./static/test.jpg')
rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
results = pytesseract.image_to_osd(rgb, output_type=Output.DICT)
# display the orientation information
print("[INFO] detected orientation: {}".format(
	results["orientation"]))
print("[INFO] rotate by {} degrees to correct".format(
	results["rotate"]))
print("[INFO] detected script: {}".format(results["script"]))

rotated = imutils.rotate_bound(image, angle=results["rotate"])
# show the original image and output image after orientation
# correction
cv2.imshow("Original", image)
cv2.imshow("Output", rotated)
cv2.waitKey(0)

#=================

conn = sqlite3.connect('card.db')

df = pd.read_sql('select name, setCode, artist from cards', conn)

names_list = []
for key, row in df.iterrows():
    try:
        full_name = row['name'] + ' ' + row['setCode'] + ' ' + row['artist']
    except:
        continue
    names_list.append(full_name)

unique_cards = pd.read_sql('select name from cards_unique', conn)



img = cv2.imread('./static/current_scan (1).jpg')

    
dim = (img.shape[1], img.shape[0])
top_img = img[0:400, 0:dim[0]]
bottom_img = img[dim[1]-400:dim[1], 0:dim[0]]



scale_percent = 700 # percent of original size
width = int(bottom_img.shape[1] * scale_percent / 100)
height = int(bottom_img.shape[0] * scale_percent / 100)
dim_bottom = (width, height)

scale_percent = 100 # percent of original size
width = int(top_img.shape[1] * scale_percent / 100)
height = int(top_img.shape[0] * scale_percent / 100)
dim_top = (width, height)

top_img_scaled = cv2.resize(top_img, dim_top, interpolation = cv2.INTER_AREA)
bottom_img_scaled = cv2.resize(bottom_img, dim_bottom, interpolation = cv2.INTER_AREA)

cv2.imwrite('./static/cropped.jpg', bottom_img_scaled)
cv2.imwrite('./static/cropped_top.jpg', top_img_scaled)

#gray_img = get_grayscale(img)
top_img_scaled = get_grayscale(top_img_scaled)
bottom_img_scaled = get_grayscale(bottom_img_scaled)
#opening_img = opening(gray_img)

#gray_img_scaled = get_grayscale(img_scaled)
#opening_img_scaled = opening(gray_img_scaled)

for i in range(0,12):
    i = 11

    custom_config = r'--oem 3 --psm '+str(i)
    try:
        text_top = pytesseract.image_to_string(top_img_scaled, config=custom_config).strip()
        text_top = text_top[:text_top.find('\n')]
        text_bottom = pytesseract.image_to_string(bottom_img_scaled, config=custom_config).strip()
    except:
        continue
    #text_original_scaled = pytesseract.image_to_string(opening_img_scaled, config=custom_config)
    #text_gray_img_scaled = pytesseract.image_to_string(gray_img_scaled, config=custom_config)

    print('--------------')
    print(text_top)
    text_bottom_index = text_bottom.find('+')
    text_bottom = text_bottom[text_bottom_index-4:]
    print(text_bottom)
    print(custom_config)
    print('-------------')
    

    '''
    max_score = 0
    for key, row in unique_cards.iterrows():
        ratio = fuzz.ratio(text_top, row['name'])
        #print(ratio)
        
        
        if ratio > max_score:
            best_text = row['name']
            #best_text_type = text_type
            max_score = ratio
            print(ratio, '\t', '\t', best_text)
    print('finished')
    print(text_top)
    input()
    '''
    max_score = 0
    for full_name in names_list:
        
        ratio = fuzz.ratio(text_top + ' ' + text_bottom, full_name)
        #print(ratio)
        
        if ratio > max_score:
            best_text = full_name
            #best_text_type = text_type
            max_score = ratio
            print(ratio, '\t', '\t', best_text)
    input()
    continue
