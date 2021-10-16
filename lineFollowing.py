#!/usr/bin/python3

import time
import grovepi
from brickpi3 import *

rLF = 3
lLF = 2

delay = 0.01

BP = BrickPi3()

rM = BP.PORT_D
lM = BP.PORT_A

defaultPower = 20
correction = 5

maxPower = 30
minPower = -20
straightPower = 40

rPower = 0
lPower = 0

try:
    while True:
        try:
            # if not (grovepi.digitalRead(rLF) == 0 and grovepi.digitalRead(lLF) == 0):
            #     maxPower = 10
            right = grovepi.digitalRead(rLF)
            left = grovepi.digitalRead(lLF)
            if (right == 0 and left == 0):
                if (rPower < straightPower):
                    rPower += correction
                if (lPower < straightPower):
                    lPower += correction
            elif (right == 1 and left == 0):
                if (rPower > minPower):
                    rPower -= correction
                if (lPower < maxPower):
                    lPower += correction
            elif (right == 0 and left == 1):
                if (lPower > minPower):
                    lPower -= correction
                if (rPower < maxPower):
                    rPower += correction

            BP.set_motor_power(rM, rPower)
            BP.set_motor_power(lM, lPower)

        except IOError as error:
            print(error)

        time.sleep(delay)



except KeyboardInterrupt:
    BP.reset_all()
