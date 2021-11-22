from macro import MACRO
from time import sleep
from brickpi3 import BrickPi3
from getConfig import getConfig

macro = MACRO(BrickPi3(), getConfig())

try:
    while True:
        macro.followLine(-1)
    #while macro.imu.getValue() < 100:
        #sleep(0.12)
    #macro.stop()
    
except KeyboardInterrupt:
    macro.terminate()

macro.terminate()
