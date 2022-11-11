import cv2
import time
from random import randint
# open video0
cap = cv2.VideoCapture(0)
cap.grab()
cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
time.sleep(2)
cap.set(cv2.CAP_PROP_FOCUS, 400)
focus_values = 400
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # Display the resulting frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    fm = cv2.Laplacian(gray, cv2.CV_64F).var()
    time.sleep(.5)
    print(fm, cap.get(cv2.CAP_PROP_FOCUS))

    focus_x = randint(0,2000)
    print('setting focus', focus_x)
    cap.set(cv2.CAP_PROP_FOCUS, focus_x)

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if cv2.waitKey(1) & 0xFF == ord('p'):
        focus_values = focus_values + 100
    if cv2.waitKey(1) & 0xFF == ord('o'):
        focus_values = focus_values - 100

    cap.set(cv2.CAP_PROP_FOCUS, focus_values)
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()