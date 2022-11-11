import maestro
import time
center = 5925

def set_target(target_x):
    print('setting', target_x)
    servo.setTarget(1,target_x)

servo = maestro.Controller('COM3')

servo.setSpeed(1,20)

set_target(center)
time.sleep(3)
set_target(center+400)
time.sleep(3)
set_target(center)
time.sleep(3)
set_target(center-400)
time.sleep(3)
set_target(center)
#time.sleep(3)
servo.close()

