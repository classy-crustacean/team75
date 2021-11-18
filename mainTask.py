from time import sleep
from brickpi3 import *
from getConfig import *
from macro import *

BP = BrickPi3()
config = getConfig()

macro = MACRO(BP, config)

try:
    while True:
        print(macro.getLinePositions())
except KeyboardInterrupt:
    macro.terminate()
