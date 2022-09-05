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

sets = pd.read_sql('select setCode from cards', conn).drop_duplicates()
sets = sets.values


recognized_cards = []

magic_card_detector.load()



def get_text():
    img = cv2.imread('./static/current_scan.tiff')
    
    #img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    

        
    dim = (img.shape[1], img.shape[0])
    #top_img = img[0:400, 0:dim[0]]
    bottom_img = img[dim[1]-500:dim[1], 0:dim[0]]


    #scale_percent = 75 # percent of original size
    #width = int(top_img.shape[1] * scale_percent / 100)
    #height = int(top_img.shape[0] * scale_percent / 100)
    #dim_top = (width, height)

    scale_percent = 200 # percent of original size
    width = int(bottom_img.shape[1] * scale_percent / 100)
    height = int(bottom_img.shape[0] * scale_percent / 100)
    dim_bottom = (width, height)




    #top_img_scaled = cv2.resize(top_img, dim_top, interpolation = cv2.INTER_AREA)
    bottom_img_scaled = cv2.resize(bottom_img, dim_bottom, interpolation = cv2.INTER_AREA)

    #top_img_scaled = get_grayscale(top_img_scaled)

    bottom_img_scaled = cv2.bitwise_not(bottom_img_scaled)
    
    cv2.imwrite('./static/cropped.tiff', bottom_img_scaled)
    #cv2.imwrite('./static/cropped_top.tiff', top_img_scaled)

    #gray_img_scaled = get_grayscale(img_scaled)
    #opening_img_scaled = opening(gray_img_scaled)



    
    custom_config_top = r'--oem 3 --psm 6'
    custom_config_bottom = r'--oem 3 --psm 6'
    try:
        #text_top = pytesseract.image_to_string(top_img_scaled, config=custom_config_top).strip()
        #text_top = text_top[:text_top.find('\n')]
        text_bottom = pytesseract.image_to_string(bottom_img_scaled, config=custom_config_bottom).strip()
        text_bottom = text_bottom.replace('Wizards of the Coast','')
        #print(text_top)
        print(text_bottom)
        
        
    except Exception as e:
        print(e)


    set_found = None
    
    for set_code in sets:
        set_code = set_code[0]
        if set_code.lower()+' ' in text_bottom.lower():
            
            set_found = set_code
            print('found set code', set_code)
            break

    if set_found is None:
        print('set code not found')
    print('\n\n')
    
    return set_found, text_bottom


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
        
        #set_found, bottom_text = get_text()
        
        magic_card_detector.set_found = None
        
        
        magic_card_detector.run()
        end = time.time()

        print("full run took", end - start, 'seconds')
        
        print('recognized card as', magic_card_detector.card_detected)

        recognized_cards = [magic_card_detector.card_detected] + recognized_cards

        magic_card_detector.card_detected = None
        magic_card_detector.set_found = None
        #ecognized = magic_card_detector.return_recognized()
        #print(recognized)
        #for image in magic_card_detector.card_detector.test_images:
            #print(image.return_recognized()[0].name)
        
        
    return render_template('index.html', recognized_cards=recognized_cards)

if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = False
    app.run(host='0.0.0.0', debug=False)





