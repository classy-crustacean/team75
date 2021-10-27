#!/usr/bin/python3

from os import setpriority
import time
import math
import grovepi
from brickpi3 import *

# Loop delay, controls how often the main loop is run
delay = 0.001

# Default motor power
defaultPower = 0
# Amount the power changes by each cycle
correction = 5

# Maximum power in curves 
maxPower = 30
maxSpeed = 100 # mm/s
# Maximum power in straightaways
straightPower = 40
straightSpeed = 120 # mm/s

# Maximum power in reverse
reversePower = 5
reverseSpeed = 40 # mm/s

hallToCargoDistance = 150
wheelDiameter = 60 # mm

radii = {1: 127.0,
         2: 44.45,
         3: 38.1}

class lineFollower:

    def __init__(self, BP, ports):
        print("initializing line follower")
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
        self.degPermm = 360 / (wheelDiameter * math.pi)
        print("line follower initialized")
    
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
            time.sleep(0.25)
        except IOError as error:
            print(error)
    
    def mmdeg(self, millimeters):
        return int(millimeters * self.degpermm)
    
    def forwardPrecise(self, millimeters):
        t = millimeters / straightSpeed
        self.straight()
        time.sleep(t)
        self.brake()
    
    def changePower(self, motor, targetPower):
        if (motor['power'] < targetPower):
            self.setPower(motor, motor['power'] + correction)
        elif (motor['power'] > targetPower):
            self.setPower(motor, motor['power'] - correction)

    def setSpeed(self, motor, targetSpeed):
        try:
            self.BP.set_motor_dps(motor['port'], -self.mmDeg(targetSpeed))
        except IOError as error:
            print(error)

    def straight(self):
        self.setSpeed(self.motors['right'], straightSpeed)
        self.setSpeed(self.motors['left'], straightSpeed)
        # self.changePower(self.motors['right'], straightPower)
        # self.changePower(self.motors['left'], straightPower)
        # if (self.motors['right']['power'] < self.motors['left']['power']):
            # self.changePower(self.motors['right'], self.motors['left']['power'])
        # elif (self.motors['right']['power'] > self.motors['left']['power']):
            # self.changePower(self.motors['left'], self.motors['right']['power'])

    def right(self):
        self.setSpeed(self.motors['right'], -0.5 * maxSpeed)
        self.setSpeed(self.motors['left'], maxSpeed)
        # self.changePower(self.motors['right'], -maxPower)
        # self.changePower(self.motors['left'], maxPower)

    def left(self):
        self.setSpeed(self.motors['right'], maxSpeed)
        self.setSpeed(self.motors['left'], -0.5 * maxSpeed)
        # self.changePower(self.motors['right'], maxPower)
        # self.changePower(self.motors['left'], -maxPower)

    def brake(self):
        self.setSpeed(self.motors['right'], 0)
        self.setSpeed(self.motors['left'], 0)
        # self.setPower(self.motors['right'], 0)
        # self.setPower(self.motors['left'], 0)
    
    def reverse(self):
        self.setSpeed(self.motors['right'], -reverseSpeed)
        self.setSpeed(self.motors['left'], -reverseSpeed)
        # self.changePower(self.motors['right'], -reversePower)
        # self.changePower(self.motors['left'], -reversePower)
    
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
            # self.forwardPrecise(hallToCargoDistance + radii[shape])
            self.straight()
            time.sleep(0.1)
            self.brake()
            self.openLatch()
            self.openCable()

        except KeyboardInterrupt:
            self.stop()
    
    def restart(self):
        try:
            self.brake()
            self.closeLatch()
            self.openCable()
            # while the touch sensor isn't pressed, do nothing
            while self.getTouch() == 0:
                time.sleep(.1)
            self.closeCable()
            time.sleep(1)
            # while the touch sensor isn't pressed, do nothing
            while self.getTouch() == 0:
                time.sleep(.1)

        except KeyboardInterrupt:
            self.stop()
