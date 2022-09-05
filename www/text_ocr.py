from audioop import mul
from cgitb import text
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
from multiprocessing import Process
import multitasking
import time
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

best_ratio = 0
best_text = ''



@multitasking.task
def get_best_match(this_input):
    print('STARTING TASK')
    text_top, text_bottom, names_list = this_input
    max_score = 0
    global best_ratio
    global best_text
    for set_code, full_name in names_list:
        if set_code not in text_bottom:
            continue
        ratio = fuzz.ratio((text_top + '\n' + text_bottom).lower(), full_name.lower())
        #print((text_top + '\n' + text_bottom).lower())
        #print(ratio)
        
        if ratio >= best_ratio:
            best_text = full_name
            #best_text_type = text_type
            best_ratio = ratio
            print(ratio, '\t', '\t', best_text)

def chunkify(lst, n):
    return [lst[i::n] for i in range(n)]


    
    

if __name__ == '__main__':
    
    conn = sqlite3.connect('card.db')

    df = pd.read_sql('select name, number, setCode, artist from cards', conn)

    sets = pd.read_sql('select setCode from cards', conn).drop_duplicates()
    sets = sets.values
    print(sets)

    names_list = []
    for key, row in df.iterrows():
        try:
            full_name = row['name'] + ' ' + row['number']+ ' '+row['setCode'] + ' ' + row['artist'] 
        except:
            continue
        names_list.append( ( row['setCode'], full_name))
    chunks = chunkify(names_list, 4)
    #unique_cards = pd.read_sql('select name from cards_unique', conn)
    
    for image_num in range(0,8):

        start = time.time()
        img = cv2.imread('./image'+str(image_num)+'.tiff')

        img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
        

            
        dim = (img.shape[1], img.shape[0])
        top_img = img[0:400, 0:dim[0]]
        bottom_img = img[dim[1]-500:dim[1], 0:dim[0]]


        scale_percent = 75 # percent of original size
        width = int(top_img.shape[1] * scale_percent / 100)
        height = int(top_img.shape[0] * scale_percent / 100)
        dim_top = (width, height)

        scale_percent = 200 # percent of original size
        width = int(bottom_img.shape[1] * scale_percent / 100)
        height = int(bottom_img.shape[0] * scale_percent / 100)
        dim_bottom = (width, height)




        top_img_scaled = cv2.resize(top_img, dim_top, interpolation = cv2.INTER_AREA)
        bottom_img_scaled = cv2.resize(bottom_img, dim_bottom, interpolation = cv2.INTER_AREA)

        top_img_scaled = get_grayscale(top_img_scaled)

        bottom_img_scaled = cv2.bitwise_not(bottom_img_scaled)
        #top_img_scaled = cv2.bitwise_not(top_img_scaled)

        
        #bottom_img_scaled = get_grayscale(bottom_img_scaled)
        #(thresh, top_img_scaled) = cv2.threshold(top_img_scaled, 80, 255, cv2.THRESH_BINARY)
        #(thresh, bottom_img_scaled) = cv2.threshold(bottom_img_scaled, 180, 255, cv2.THRESH_BINARY)


        #top_img_scaled = cv2.bitwise_not(top_img_scaled)

        #opening_img = opening(gray_img)

        cv2.imwrite('./static/cropped.tiff', bottom_img_scaled)
        cv2.imwrite('./static/cropped_top.tiff', top_img_scaled)

        #gray_img_scaled = get_grayscale(img_scaled)
        #opening_img_scaled = opening(gray_img_scaled)



        
        custom_config_top = r'--oem 3 --psm 6'
        custom_config_bottom = r'--oem 3 --psm 6'
        try:
            text_top = pytesseract.image_to_string(top_img_scaled, config=custom_config_top).strip()
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
        continue
            
        #text_original_scaled = pytesseract.image_to_string(opening_img_scaled, config=custom_config)
        #text_gray_img_scaled = pytesseract.image_to_string(gray_img_scaled, config=custom_config)

        '''
        print('--------------')
        print(text_top)
        text_bottom_index = text_bottom.find('+')
        text_bottom = text_bottom[text_bottom_index-4:]
        print(text_bottom)
        #print(custom_config)

        print('-------------')
        '''


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
        for chunk_num in list(range(0,4)):
            get_best_match([text_top, text_bottom, chunks[chunk_num]])

        multitasking.wait_for_tasks()
        print(best_ratio, best_text)
        end = time.time()
        print('time taken', end-start)
        #input()

        
        best_ratio = 0
        best_text = ''
    