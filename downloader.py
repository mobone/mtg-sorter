
from bs4 import BeautifulSoup
import re
import numpy as np
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from time import sleep
import pandas as pd

import datetime

import yfinance
import threading
import urllib
import urllib.request
import os
import pandas as pd
import sqlite3
import multitasking
conn = sqlite3.connect('all_cards.db')
#options = webdriver.ChromeOptions()
#options.add_argument("start-maximized")
#options.add_argument("--headless")
#options.add_argument("--log-level=3")
#options.add_experimental_option("excludeSwitches", ["enable-automation"])
#options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome()

#multitasking.set_max_threads(4)


@multitasking.task
def download_image(set_acronym, card_name, card_url, set_number):

    downloaded_size = 0
    try:
         
        downloaded_size = os.stat("./magic_card_detector/cards/%s - %s.png" % (set_acronym, card_name)).st_size
    except:
        pass

    try:
        original_filesize = urllib.request.urlopen(card_url).length
        while downloaded_size != original_filesize:
            
            print('caught mismatch', card_url, downloaded_size, original_filesize)
            
            urllib.request.urlretrieve(card_url, "./magic_card_detector/cards/%s - %s.png" % (set_acronym, card_name))
            original_filesize = urllib.request.urlopen(card_url).length
            downloaded_size = os.stat("./magic_card_detector/cards/%s - %s.png" % (set_acronym, card_name)).st_size
    except Exception as e:
        print('got exception', e)
        print(set_acronym, card_name, card_url)
    #print('downloaded image', card_url)

    
    



def download_image_wrapper(card_input, set_number):
    set_acronym, card_name, card_url = card_input
    download_image(set_acronym, card_name, card_url, set_number)



for set_number in range(0,400):
    url = 'https://www.mtgpics.com/set?set='+str(set_number)


    #driver = webdriver.Chrome(executable_path='C:\\Users\\nbrei\\Documents\\GitHub\\OptimalEve\\chromedriver.exe', options=options)
    print('getting', url)
    driver.get(url)
    
    if ' art' in driver.title.lower():
        continue
    if ' promo' in driver.title.lower():
        continue
    sleep(1)
    cards = driver.find_elements_by_tag_name('img')

    cards_db = []
    card_tuples = []
    set_acronym = ''
    
    for card in cards:
        card_url = card.get_attribute('src')
        card_text = card.get_attribute("alt")
        if ' - ' not in card_text:
            continue

        card_url = card_url.replace('reg', 'big')
        card_name = card_text.split(' - ')[0]
        #card_name = card_name.replace('/', '|')
        #card_name = card_name.replace(':', '#')
        for i in [':', '(', ')', '//', '/', '?','!', '|']:
            card_name = card_name.replace(i, '')
        #print('found card', card_name)
        set_name = card_text.split(' - ')[1]
        set_acronym = card_url.split('/')[5]
        #isExist = os.path.exists('./cards/'+set_acronym)

        #if isExist==False:
        #    os.mkdir('./cards/'+set_acronym)
        
        
        card_tuple = (set_acronym, card_name, card_url)
        #cards_db.append(card_dict)
        card_tuples.append(card_tuple)
    '''
    for card in card_tuples:
        download_image_wrapper(card, set_number)
    '''

    try:
        urllib.request.urlretrieve('https://www.mtgpics.com/graph/sets/symbols/%s-c.png' % set_acronym.lower(), "./magic_card_detector/set_symbols/%s-c.png" % (set_acronym.lower()))
    except Exception as e:
        print(e)
        print('set number', set_number)
        print('https://www.mtgpics.com/graph/sets/symbols/%s-c.png' % set_acronym.lower())
        pass
    try:
        urllib.request.urlretrieve('https://www.mtgpics.com/graph/sets/symbols/%s-u.png' % set_acronym.lower(), "./magic_card_detector/set_symbols/%s-u.png" % (set_acronym.lower()))
    except:
        pass
    try:
        urllib.request.urlretrieve('https://www.mtgpics.com/graph/sets/symbols/%s-r.png' % set_acronym.lower(), "./magic_card_detector/set_symbols/%s-r.png" % (set_acronym.lower()))
    except:
        pass
    try:
        urllib.request.urlretrieve('https://www.mtgpics.com/graph/sets/symbols/%s-mr.png' % set_acronym.lower(), "./magic_card_detector/set_symbols/%s-mr.png" % (set_acronym.lower()))
    except:
        pass

    multitasking.wait_for_tasks()


    #df = pd.DataFrame.from_dict(cards_db)
    #df.to_sql('cards', conn, if_exists='append')
