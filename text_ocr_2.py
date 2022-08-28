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
for img_filename in file_names:
    img = cv2.imread('./test_cards/'+img_filename)

    print('====================')

    print(img_filename)
    
    dim = (img.shape[1], img.shape[0])
    print(dim)
    img = img[0:300, 0:dim[0]]
    #cv2.imshow('asdf', img)
    
    img = get_grayscale(img)
    #thresh = cv2.threshold(img, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY_INV)[1]
    #thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    thresh = thresholding(img)
    blur = cv2.GaussianBlur(thresh, (3,3), 0)
    result = 255 - blur 

    text_1 = pytesseract.image_to_string(result, config='--oem 3 --psm 6')

    custom_config = r'--oem 3 --psm 4'
    text_2 = pytesseract.image_to_string(result, config=custom_config)
    max_match = 0
    for text, text_type in [(text_1, 'text_1'),(text_2, 'text_2')]:
        print(text)
        if text is None or text == '':
            continue
        print('----------------')
        print(text_type)
        print(text)
        print('----------------')
        
        for key, row in df.iterrows():

            ratio = fuzz.ratio(text, row.values[0])
            if ratio<55:
                continue
            if ratio > max_match:
                best_text = row.values[0]
                best_text_type = text_type
                max_match = ratio
                print(ratio, '\t', best_text_type, '\t', best_text)

    print('\nbest card:', max_match, best_text_type,'\t', best_text)
    

end = time.time()
print( (end-start) / len(file_names))