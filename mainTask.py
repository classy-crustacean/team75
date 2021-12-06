from os import EX_CANTCREAT, wait
from time import sleep
from brickpi3 import BrickPi3
from getConfig import getConfig
from macro import MACRO


sites = {'a': 1, 'b': 1, 'c': 1}

macro = MACRO(BrickPi3(), getConfig())


def getTarget():
    while True:
        try:
            target = input("Input the target drop-off zone: ")
            return {'pos': list(sites.keys()).index(target.lower()), 'bias': sites[target.lower()]}
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except:
            print("Error! Must enter A, B, or C")

def continueChoice():
    try:
        while True:
                choice = input("Drive another lap? (Y/N) ")
                if (choice.lower() == 'n'):
                    raise KeyboardInterrupt
                elif (choice.lower() == 'y'):
                    break
                else:
                    print("\nError! Must enter Y or N!\n")
    except KeyboardInterrupt:
        raise KeyboardInterrupt

def waitForMagnet():
    value = macro.imu.getValue()
    while (value < 100):
        sleep(0.13)
        value = macro.imu.getValue()
    sleep(0.13)
    value = macro.imu.getValue()
    while (value < -100 or value >= 0):
        sleep(0.13)
        value = macro.imu.getValue()
    
try:
    while True:
        target = getTarget()
        print("position: %d\nbias: %d\n" % (target['pos'], target['bias']))
        input("place cargo in macro, then press any key to start")
        macro.followLine(-1)
        for i in range(target['pos']):
            waitForMagnet()
        macro.setBias(target['bias'])
        waitForMagnet()
        macro.stop()
        macro.dropCargo()
        macro.followLine(-1)
        waitForMagnet()
        macro.stop()
except KeyboardInterrupt:
    print("\nDone!")
