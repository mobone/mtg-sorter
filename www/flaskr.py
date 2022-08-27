from flask import Flask, render_template, request, url_for, flash, redirect
import os
import ScanCard


app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(24).hex()


@app.route('/scan-card')
def scan_card():
    ScanCard.scan_card()
    return "card scanned"
    


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print('got post form')
        scan_card()
        print('card scanned')
    return render_template('index.html')

if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host='0.0.0.0', debug=True)





