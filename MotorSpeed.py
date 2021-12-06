from brickpi3 import BrickPi3
from getConfig import getConfig
from macro import MACRO

target = 20
distance = 200

macro = MACRO(BrickPi3(), getConfig())

try:
    macro.driveForward(target, distance)
    macro.terminate()
except KeyboardInterrupt:
    macro.terminate()
