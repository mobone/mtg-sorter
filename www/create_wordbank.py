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


conn = sqlite3.connect('card.db')

df = pd.read_sql('select name, setCode, artist from cards', conn)

all_words = []
for key, row in df.iterrows():
    for item in ['name', 'setCode', 'artist']:
        item_text = row[item]
        #print(item_text)
        try:
            for word in item_text.split(' '):
                all_words.append(word)
        except:
            pass

all_words = set(all_words)
print(all_words)

with open('test_data.txt', 'w') as f:
    for word in all_words:
        try:
            f.write(word+' ')
        except:
            pass