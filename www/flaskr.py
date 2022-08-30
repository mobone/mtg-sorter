from flask import Flask, render_template, request, url_for, flash, redirect, make_response
import os
import ScanCard
import base64
import magic_card_detector
import time
import cv2
import pytesseract
from os import walk
from utils import *

from fuzzywuzzy import fuzz
import sqlite3
import os
import pandas as pd
import time


app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(24).hex()

conn = sqlite3.connect('/home/admn/Documents/mtg-sorter/www/card.db')
df = pd.read_sql('select name from cards_unique', conn)

recognized_cards = []



def get_text():
    img = cv2.imread('./static/current_scan.jpg')

    
    dim = (img.shape[1], img.shape[0])

    img = img[0:200, 0:dim[0]]

    cv2.imwrite('/home/admn/Documents/mtg-sorter/cropped.jpg', img)
    
    scale_percent = 50 # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)

    img_scaled = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

    gray_img = get_grayscale(img)
    opening_img = opening(gray_img)

    gray_img_scaled = get_grayscale(img_scaled)
    opening_img_scaled = opening(gray_img_scaled)
    
    custom_config = r'--oem 3 --psm 4'
    
    text_gray_img = pytesseract.image_to_string(gray_img, config=custom_config)
    text_original_scaled = pytesseract.image_to_string(opening_img_scaled, config=custom_config)
    text_gray_img_scaled = pytesseract.image_to_string(gray_img_scaled, config=custom_config)

    
    max_score = 0
    best_text = None
    best_text_type = None
    best_text = None
    
    #for text, text_type in [(text_original_scaled, 'original_scaled'),(text_gray_img, 'gray'), (text_gray_img_scaled, 'gray_scaled')]:
    for text, text_type in [(text_gray_img, 'gray')]:
        print(text)
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

    
    return (max_score, best_text_type, best_text)


@app.route('/scan-card')
def scan_card():
    ScanCard.scan_card()
    return "card scanned"

@app.route('/display-current')
def display_current():
    with open('/static/current_scan.jpg', 'rb') as f:
        image_binary = f.read()
        response = make_response(base64.b64encode(image_binary))
        
        response.headers.set('Content-Type', 'image/jpg')
        response.headers.set('Content-Disposition', 'attachment', filename='current_scan.jpg')

        return response


@app.route('/', methods=['GET', 'POST'])
def index():
    global recognized_cards
    if request.method == 'POST':
        start = time.time()
        print('got post form')
        scan_card()
        print('card scanned')
        
        best_score, best_text_type, best_text = get_text()
        print('got text of', best_text)
        magic_card_detector.best_text_recognized = best_text
        
        magic_card_detector.load()
        magic_card_detector.run()
        end = time.time()

        print("full run took", end - start, 'seconds')
        
        print('recognized card as', magic_card_detector.card_detected)

        recognized_cards = [magic_card_detector.card_detected] + recognized_cards

        magic_card_detector.card_detected = None
        magic_card_detector.best_text_recognized = None
        #ecognized = magic_card_detector.return_recognized()
        #print(recognized)
        #for image in magic_card_detector.card_detector.test_images:
            #print(image.return_recognized()[0].name)
        
        
    return render_template('index.html', recognized_cards=recognized_cards)

if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = False
    app.run(host='0.0.0.0', debug=False)





