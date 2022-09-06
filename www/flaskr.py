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
from markupsafe import Markup


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

def get_mana_symbols(mana_cost):

    mana_cost = mana_cost.replace('{0}', '<img src="./static/symbols/B00 - Colorless Mana - Zero.svg">')
    mana_cost = mana_cost.replace('{1}', '<img src="./static/symbols/B01 - Colorless Mana - One.svg">')
    mana_cost = mana_cost.replace('{2}', '<img src="./static/symbols/B02 - Colorless Mana - Two.svg">')
    mana_cost = mana_cost.replace('{3}', '<img src="./static/symbols/B03 - Colorless Mana - Three.svg">')
    mana_cost = mana_cost.replace('{4}', '<img src="./static/symbols/B04 - Colorless Mana - Four.svg">')
    mana_cost = mana_cost.replace('{5}', '<img src="./static/symbols/B05 - Colorless Mana - Five.svg">')
    mana_cost = mana_cost.replace('{6}', '<img src="./static/symbols/B06 - Colorless Mana - Six.svg">')
    mana_cost = mana_cost.replace('{7}', '<img src="./static/symbols/B07 - Colorless Mana - Seven.svg">')
    mana_cost = mana_cost.replace('{8}', '<img src="./static/symbols/B08 - Colorless Mana - Eight.svg">')
    mana_cost = mana_cost.replace('{9}', '<img src="./static/symbols/B09 - Colorless Mana - Nine.svg">')
    mana_cost = mana_cost.replace('{10}', '<img src="./static/symbols/B10 - Colorless Mana - Ten.svg">')
    mana_cost = mana_cost.replace('{11}', '<img src="./static/symbols/B11 - Colorless Mana - Eleven.svg">')
    mana_cost = mana_cost.replace('{12}', '<img src="./static/symbols/B12 - Colorless Mana - Twelve.svg">')
    mana_cost = mana_cost.replace('{13}', '<img src="./static/symbols/B13 - Colorless Mana - Thirteen.svg">')
    mana_cost = mana_cost.replace('{14}', '<img src="./static/symbols/B14 - Colorless Mana - Fourteen.svg">')
    mana_cost = mana_cost.replace('{15}', '<img src="./static/symbols/B15 - Colorless Mana - Fifteen.svg">')
    mana_cost = mana_cost.replace('{16}', '<img src="./static/symbols/B16 - Colorless Mana - Sixteen.svg">')
    mana_cost = mana_cost.replace('{17}', '<img src="./static/symbols/B17 - Colorless Mana - Seventeen.svg">')
    mana_cost = mana_cost.replace('{18}', '<img src="./static/symbols/B18 - Colorless Mana - Eighteen.svg">')
    mana_cost = mana_cost.replace('{19}', '<img src="./static/symbols/B19 - Colorless Mana - Nineteen.svg">')
    mana_cost = mana_cost.replace('{20}', '<img src="./static/symbols/B20 - Colorless Mana - Twenty.svg">')

    mana_cost = mana_cost.replace('{W}', '<img src="./static/symbols/A01 - Colored Mana - White.svg">')
    mana_cost = mana_cost.replace('{U}', '<img src="./static/symbols/A02 - Colored Mana - Blue.svg">')
    mana_cost = mana_cost.replace('{B}', '<img src="./static/symbols/A03 - Colored Mana - Black.svg">')
    mana_cost = mana_cost.replace('{R}', '<img src="./static/symbols/A04 - Colored Mana - Red.svg">')
    mana_cost = mana_cost.replace('{G}', '<img src="./static/symbols/A05 - Colored Mana - Green.svg">')
    mana_cost = mana_cost.replace('{S}', '<img src="./static/symbols/A06 - Colored Mana - Snow.svg">')


    
    return Markup(mana_cost)

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
        conn = sqlite3.connect('/home/admn/Documents/mtg-sorter/www/card.db')
        sql = 'select * from cards where name == "%s" and setCode == "%s"' % (magic_card_detector.card_detected.split(' - ')[1], magic_card_detector.card_detected.split(' - ')[0].upper())
        
        print(sql)
        card_details = pd.read_sql(sql, conn).head(1)

        if len(card_details) == 0:
            print('could not find card in card database, searching by name alone instead')
            sql = 'select * from cards where name == "%s"' % (magic_card_detector.card_detected.split(' - ')[1])
            print(sql)
            card_details = pd.read_sql(sql, conn).head(1)

        print(card_details)
        card_dict = {
            'card_name': str(card_details['name'].values[0]), 
            'mana_cost': str(card_details['manaCost'].values[0]),
            'mana_cost_html': get_mana_symbols(str(card_details['manaCost'].values[0])),
            'rarity': str(card_details['rarity'].values[0])
        }
        print(card_dict)
        recognized_cards = [card_dict] + recognized_cards

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





