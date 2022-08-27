from flask import Flask, render_template, request, url_for, flash, redirect
import os

import cv2 #sudo apt-get install python-opencv
import numpy as py
import os
import sys
import time
import argparse
from RpiCamera import Camera
from Focuser import Focuser
# from AutoFocus import AutoFocus



app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(24).hex()


@app.route('/scan-card')
def scan_card():
    camera = Camera()
    #focuser = Focuser(10)
    cv2.imwrite("current_card.jpg"), camera.getFrame()


@app.route('/', methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        print('got post form')
    return render_template('index.html')

if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host='0.0.0.0', debug=True)





