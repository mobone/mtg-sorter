from RpiCamera import Camera
import cv2
from Focuser import Focuser


focuser = Focuser(10)

camera = Camera()
cv2.imwrite("current_card.jpg", camera.getFrame())