#!/usr/bin/python3

from os import setpriority
import time
import math
import grovepi
from brickpi3 import *

# Loop delay, controls how often the main loop is run
delay = 0.01

# Default motor power
defaultPower = 0
# Amount the power changes by each cycle
correction = 5

# Maximum power in curves 
maxPower = 30
# Maximum power in straightaways
straightPower = 40

# Maximum power in reverse
reversePower = 5

hallToCargoDistance = 125

radii = {1: 127.0,
         2: 44.45,
         3: 38.1}

class lineFollower:

    def __init__(self, BP, ports):
        self.BP = BP
        self.motors = {}
        self.motors['right'] = {'port': ports['right drive motor'],
                                'power': 0}
        self.motors['left'] = {'port': ports['left drive motor'],
                                'power': 0}
        self.motors['latch'] = {'port': ports['latch motor'],
                                'position': 0}
        self.motors['cable'] = {'port': ports['cable motor'],
                                'position': 0}

        self.rLF = ports['right line finder']
        self.lLF = ports['left line finder']
        self.hall = ports['hall effect']
        self.ultrasonic = ports['ultrasonic']
        self.touch = ports['touch']
        self.BP.set_sensor_type(self.touch, BP.SENSOR_TYPE.TOUCH)
        time.sleep(5)
    
    def stop(self):
        try:
            self.BP.reset_all()
        except IOError as error:
            print(error)
    
    def setPower(self, motor, power):
        try:
            self.BP.set_motor_power(motor['port'], power)
            motor['power'] = power
        except IOError as error:
            print(error)
    
    def setPosition(self, motor, position):
        try:
            self.BP.set_motor_position(motor['port'], position)
            motor['position'] = position
        except IOError as error:
            print(error)
    
    def forwardPrecise(self, millimeters):
        try:
            degrees = int(millimeters / (80 * math.pi) * 360)
            self.BP.set_motor_position_relative(self.motors['right']['port'], degrees)
            self.BP.set_motor_position_relative(self.motors['left']['port'], degrees)
        except IOError as error:
            print(error)
    
    def changePower(self, motor, targetPower):
        if (motor['power'] < targetPower):
            self.setPower(motor, motor['power'] + correction)
        elif (motor['power'] > targetPower):
            self.setPower(motor, motor['power'] - correction)
    
    def straight(self):
        self.changePower(self.motors['right'], straightPower)
        self.changePower(self.motors['left'], straightPower)
        if (self.motors['right']['power'] < self.motors['left']['power']):
            self.changePower(self.motors['right'], self.motors['left']['power'])
        elif (self.motors['right']['power'] > self.motors['left']['power']):
            self.changePower(self.motors['left'], self.motors['right']['power'])

    def right(self):
        self.changePower(self.motors['right'], -maxPower)
        self.changePower(self.motors['left'], maxPower)

    def left(self):
        self.changePower(self.motors['right'], maxPower)
        self.changePower(self.motors['left'], -maxPower)

    def brake(self):
        self.setPower(self.motors['right'], 0)
        self.setPower(self.motors['left'], 0)
    
    def reverse(self):
        self.changePower(self.motors['right'], -reversePower)
        self.changePower(self.motors['left'], -reversePower)
    
    def openLatch(self):
        self.setPosition(self.motors['latch'], 0)

    def closeLatch(self):
        self.setPosition(self.motors['latch'],  90)

    def openCable(self):
        self.setPosition(self.motors['cable'],  0)

    def closeCable(self):
        self.setPosition(self.motors['cable'], 90)

    def getTouch(self):
        try:
            return self.BP.get_sensor(self.touch)
        except IOError as error:
            print(error)
    
    def getHall(self):
        try:
            return grovepi.digitalRead(self.hall)
        except IOError as error:
            print(error)

    def getRightLine(self):
        try:
            return grovepi.digitalRead(self.rLF)
        except IOError as error:
            print(error)

    def getLeftLine(self):
        try:
            return grovepi.digitalRead(self.lLF)
        except IOError as error:
            print(error)

    def followLine(self):

        try:
            while True:
                # if not (grovepi.digitalRead(rLF) == 0 and grovepi.digitalRead(lLF) == 0):
                #     maxPower = 10
                right = self.getRightLine()
                left = self.getLeftLine()
                if (self.getHall() == 0):
                    break
                # straightaway
                if (right == 0 and left == 0):
                    self.straight()
                # line curves right
                elif (right == 1 and left == 0):
                    self.right()
                # line curves left
                elif (right == 0 and left == 1):
                    self.left()

                time.sleep(delay)

        except KeyboardInterrupt:
            self.stop()
    
    def branch(self):
        try:
            while self.getRightLine() == 0 and self.getLeftLine() == 0:
                time.sleep(delay)
            
            if self.getRightLine() == 1:
                while (self.getLeftLine() == 0):
                    if (self.getRightLine() == 1):
                        self.right()
                    else:
                        self.straight()
                while (self.getLeftLine() == 1):
                    if (self.getRightLine() == 1):
                        self.right()
                    else:
                        self.straight()
            elif self.getLeftLine() == 1:
                while (self.getRightLine() == 0):
                    if (self.getLeftLine() == 1):
                        self.left()
                    else:
                        self.straight()
                while (self.getRightLine() == 1):
                    if (self.getLeftLine() == 1):
                        self.left()
                    else:
                        self.straight()
        except KeyboardInterrupt:
            self.stop()
    
    def dropOff(self, shape):
        try:
            self.brake()
            while (self.getHall() == 1):
                self.reverse()
            self.brake()
            self.forwardPrecise(hallToCargoDistance + radii[shape])
            self.openLatch()
            self.openCable()

        except KeyboardInterrupt:
            self.stop()
    
    def restart(self):
        try:
            # self.brake()
            self.closeLatch()
            self.openCable()
            # input("press Enter to close cable")
            # while the touch sensor isn't pressed, do nothing
            while self.getTouch() == 0:
                time.sleep(.1)
            self.closeCable()
            time.sleep(1)
            # input("press Enter to continue")
            # while the touch sensor isn't pressed, do nothing
            while self.getTouch() == 0:
                time.sleep(.1)

        except KeyboardInterrupt:
            self.stop()
