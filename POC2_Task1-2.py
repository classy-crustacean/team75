from macro import MACRO
from time import sleep
from brickpi3 import BrickPi3
from getConfig import getConfig

macro = MACRO(BrickPi3(), getConfig())

try:
    macro.followLine(1)
    while True:
        continue
    
except KeyboardInterrupt:
    macro.terminate()
