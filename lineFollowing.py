#!/usr/bin/python3

import time
import grovepi
from brickpi3 import *

rLF = 8
lLF = 3

delay = 0.02

BP = BrickPi3()

rM = BP.PORT_A
lM = BP.PORT_D

try:
    while True:
        try:
            if grovepi.digitalRead(rLF) == 0:
                print("right White")
                BP.set_motor_power(rM, 20)
            else:
                print("right Black")
                BP.set_motor_power(rM, -20)
           
            if grovepi.digitalRead(lLF) == 0:
                print("left White")
                BP.set_motor_power(lM, 20)
            else:
                print("right Black")
                BP.set_motor_power(lM, -20)

        except IOError as error:
            print(error)

        time.sleep(delay)



except KeyboardInterrupt:
    BP.reset_all()
