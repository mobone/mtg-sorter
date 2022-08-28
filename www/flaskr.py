from flask import Flask, render_template, request, url_for, flash, redirect, make_response
import os
import ScanCard
import base64
import magic_card_detector
import time
app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(24).hex()



magic_card_detector.load()

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
    if request.method == 'POST':

        start = time.time()
        
        print('got post form')
        scan_card()
        print('card scanned')
        
        #magic_card_detector.load()
        magic_card_detector.run()
        
        end = time.time()
        print("full run took", end - start, 'seconds')
        #ecognized = magic_card_detector.return_recognized()
        #print(recognized)
        #for image in magic_card_detector.card_detector.test_images:
            #print(image.return_recognized()[0].name)
        
        
    return render_template('index.html')

if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = False
    app.run(host='0.0.0.0', debug=False)





