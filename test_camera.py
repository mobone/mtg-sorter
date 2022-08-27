import time
import signal
import cv2
import threading
import argparse
from RpiCamera import Camera
from Focuser import Focuser
from Autofocus import FocusState, doFocus

exit_ = False

if __name__ == "__main__":
    
    camera = Camera()
    #camera.start_preview(False)
    focuser = Focuser(10)
    #focuser.verbose = args.verbose

    focusState = FocusState()
    #focusState.verbose = args.verbose
    doFocus(camera, focuser, focusState)

    while not exit_:
        frame = camera.getFrame()
        img = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        if focusState.isFinish():
            exit_ = True
    frame = camera.getFrame()
    img = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    cv2.imwrite("current_scan.jpg", img)
    camera.close()
