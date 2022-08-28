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

dir_path = './cards/'
file_names = list(os.walk('./test_cards/'))[0][2]
print(file_names)
start = time.time()
def read_text():
    img = cv2.imread('./test_cards/'+img_filename)

    print('====================')

    print(img_filename)
    
    dim = (img.shape[1], img.shape[0])

    img = img[0:300, 0:dim[0]]
    #cv2.imwrite('output.png', img)
    #input()

    scale_percent = 50 # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)

    img_scaled = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

    #print(dim)
    #input()

    gray_img = get_grayscale(img)
    opening_img = opening(gray_img)

    gray_img_scaled = get_grayscale(img_scaled)
    opening_img_scaled = opening(gray_img_scaled)
    
    custom_config = r'--oem 3 --psm 4'
    text_original = pytesseract.image_to_string(opening_img, config=custom_config)
    text_gray_img = pytesseract.image_to_string(gray_img, config=custom_config)
    text_original_scaled = pytesseract.image_to_string(opening_img_scaled, config=custom_config)
    text_gray_img_scaled = pytesseract.image_to_string(gray_img_scaled, config=custom_config)

    #text_opening_img = pytesseract.image_to_string(opening_img, config=custom_config)
    


    max = 0
    best_text = None
    best_text_type = None
    best_text = None
    #for text, text_type in [(text_original, 'original'), (text_gray_img, 'gray'), (text_original_scaled, 'original_scaled'), (text_gray_img_scaled, 'gray_scaled')]:
    for text, text_type in [(text_original_scaled, 'original_scaled'),(text_gray_img, 'gray'), (text_gray_img_scaled, 'gray_scaled')]:
        print(text)
        if text is None or text == '':
            continue
        print('----------------')
        print(text)
        print('----------------')
        #input()
        for key, row in df.iterrows():

            ratio = fuzz.ratio(text, row.values[0])
            if ratio<55:
                continue
            if ratio > max:
                best_text = row.values[0]
                best_text_type = text_type
                max = ratio
                print(ratio, '\t', best_text_type, '\t', best_text)

    print('\nbest card:', max, best_text_type,'\t', best_text)
    '''
    h, w, c = img.shape
    boxes = pytesseract.image_to_boxes(img)
    for b in boxes.splitlines():
        b = b.split(' ')
        img = cv2.rectangle(img, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)

    cv2.imshow('img', img)
    cv2.waitKey(0)
    '''
    return best_text
#end = time.time()
#print( (end-start) / len(file_names))