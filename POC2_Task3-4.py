from macro import MACRO
from time import sleep
from brickpi3 import BrickPi3
from getConfig import getConfig

macro = MACRO(BrickPi3(), getConfig())

zones = {1: 1,
         2: 0,
         3: 1}

target = 1

try:
    macro.followLine(-1)
    for i in range(1, target):
        print("awaiting magnet...")
        while (macro.imu.getValue() < 100):
            sleep(0.12)
        print("found magnet")
        macro.setBias(abs(zones[i] - 1))
        sleep(1)
        macro.setBias(-1)
        print("passed zone", i )
    while (macro.imu.getValue() < 100):
        sleep(0.12)
    macro.setBias(zones[target])
    sleep(1)
    macro.setBias(-1)
    print("waiting for magnet")
    while (macro.imu.getValue() < 100):
        sleep(0.12)
    print("found drop off point")
    print("waiting to pass magnet")
    while (macro.imu.getValue() > 100):
        sleep(0.12)
    print("passed magnet")
    macro.stop()
    macro.releaseCargo()
    print("dropped off cargo")
    print("following line to end")
    macro.followLine(-1)
    sleep(1)
    while (macro.imu.getValue() < 100):
        sleep(0.12)
    macro.stop()
    macro.terminate()
    
except:
    macro.terminate()
