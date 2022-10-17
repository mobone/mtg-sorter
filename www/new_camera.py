import cv2
import time
# open video0
cap = cv2.VideoCapture(0)
cap.grab()
cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)
time.sleep(2)


while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # Display the resulting frame
    print(cap.get(cv2.CAP_PROP_FOCUS))
    time.sleep(.5)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()