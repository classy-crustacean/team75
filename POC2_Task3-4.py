from macro import MACRO
from time import sleep
from brickpi3 import BrickPi3
from getConfig import getConfig

macro = MACRO(BrickPi3(), getConfig())

zones = {1: 1, 2: 2, 3: 1}

target = 1

try:
    macro.followLine()
    for i in range(target - 1):
        macro.setBias(zones[i + 1] % 2 + 1)
        print("awaiting magnet...")
        while (macro.imu.getValue() < 70):
            sleep(0.12)
        print("found magnet")
        print("awaiting leaving magnet...")
        sleep(0.12)
        while (macro.imu.getValue() > 70):
            sleep(0.12)
        print("left magnet")
        print("passed zone", i + 1)
    macro.setBias(1)
    while macro.imu.getValue() < 70:
        sleep(0.12)
    macro.stop()
    macro.releaseCargo()
    macro.followLine(1)
    
except KeyboardInterrupt:
    macro.terminate()
