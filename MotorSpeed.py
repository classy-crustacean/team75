from brickpi3 import BrickPi3
from getConfig import getConfig
from macro import MACRO

target = 19.72
distance = 250

macro = MACRO(BrickPi3(), getConfig())

try:
    macro.driveForward(target, distance)
    input("done! press enter to continue")
    macro.terminate()
except KeyboardInterrupt:
    macro.terminate()
