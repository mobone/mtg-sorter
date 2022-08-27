from RpiCamera import Camera
camera = Camera()
cv2.imwrite("current_card.jpg"), camera.getFrame()