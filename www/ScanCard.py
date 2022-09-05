import time
import signal
import cv2
import threading
import argparse
from RpiCamera import Camera
from Focuser import Focuser
from Autofocus import FocusState, doFocus

exit_ = False
def sigint_handler(signum, frame):
    global exit_
    exit_ = True

signal.signal(signal.SIGINT, sigint_handler)
signal.signal(signal.SIGTERM, sigint_handler)

camera = Camera()
camera.start_preview(False)
focuser = Focuser(10)

def parse_cmdline():
    parser = argparse.ArgumentParser(description='Arducam IMX519 Autofocus Demo.')

    parser.add_argument('-i', '--i2c-bus', type=int, nargs=None, required=False,
                        help='Set i2c bus, for A02 is 6, for B01 is 7 or 8, for Jetson Xavier NX it is 9 and 10.')

    parser.add_argument('-v', '--verbose', action="store_true", help='Print debug info.')

    return parser.parse_args()

def scan_card():
    exit_ = False
    #args = parse_cmdline()
    
    #focuser.verbose = args.verbose

    focusState = FocusState()
    #focusState.verbose = args.verbose
    print('focusing')
    doFocus(camera, focuser, focusState)

    while focusState.isFinish()==False:
        time.sleep(.1)
        
    time.sleep(.3)
    print('focused')
    frame = camera.getFrame()
    img = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    cv2.imwrite("./static/current_scan.tiff", img)
    
    #camera.close()

if __name__ == '__main__':
    pass