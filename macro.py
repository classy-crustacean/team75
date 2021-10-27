import brickpi3
import grovepi
import time
import math
import numpy as np
import multiprocessing as mlt

class MACRO:
    config = 0
    rightMotor = 0
    leftMotor = 0
    frontMotor = 0
    latchMotor = 0
    lineFinderCount = 4
    lineFollowProcess = 0
    bias = mlt.Value('i', 0)
    def __init__(self, BP, config):
        self.config = config
        self.rightMotor = motor(BP, config['right drive motor'], diameter=config['rear wheel diameter'])
        self.leftMotor = motor(BP, config['left drive motor'], diameter=config['rear wheel diameter'])
        self.frontMotor = motor(BP, config['front drive motor'], diameter=config['front wheel diameter'])
        self.lineFinderCount = len(config['line finders'])
        print('brug')
    
    def readLineFinders(self):
        return [0, 0, 1, 0]
    
    # I based a lot of my position code on http://robotresearchlab.com/2019/03/13/build-a-custom-pid-line-following-robot-from-scratch/#Programming_the_motors
    def getPositionUnbiased(self, lastPosition):
        values = self.readLineFinders
        num = 0
        sum = 0
        for i in range(0, len(values)):
            value = values[i]
            if (value == 1):
                num += 1
                sum += i
        
        if (num != 0):
            lastPosition = sum / num
        
        return lastPosition
    
    def getPositionRightBias(self, lastPosition):
        values = self.readLineFinders
        num = 0
        sum = 0
        for i in range(0, len(values)):
            value = values[i]
            if (value == 1):
                if (i > (len(values) - 1) / 2 and num > 0):
                    if (sum / num < (len(values) - 1) / 2):
                        num = 0
                        sum = 0
                num += 1
                sum += i
        
        if (num != 0):
            lastPosition = sum / num
        
        return lastPosition

    def getPositionLeftBias(self, lastPosition):
        values = self.readLineFinders
        num = 0
        sum = 0
        for i in reversed(range(0, len(values))):
            value = values[i]
            if (value == 1):
                if (i < (len(values) - 1) / 2 and num > 0):
                    if (sum / num > (len(values) - 1) / 2):
                        num = 0
                        sum = 0
                num += 1
                sum += i
        
        if (num != 0):
            lastPosition = sum / num
        
        return lastPosition

    def followLineLoop(self):
        Kp = self.config['Kp']
        Ki = self.config['Ki']
        Kd = self.config['Kd']
        lineFinderCount = self.lineFinderCount
        basePower = self.config['base motor power']
        leftMotor = self.leftMotor
        rightMotor = self.rightMotor

        position = 0
        error = 0
        lastError = 0
        integral = 0
        lastIntegral = 0
        derivative = 0
        iterationTime = 0
        delay = 0.02
        goal = (lineFinderCount - 1) / 2
        while True:
            if (self.bias.value == 0):
                position = self.getPositionUnbiased(self.bias.value)
            elif (self.bias.value == 1):
                position = self.getPositionLeftBias(self.bias.value)
            elif (self.bias.value == 2):
                position = self.getPositionRightBias(self.bias.value)
            error = goal - position
            integral = integral + error * delay
            derivative = (error - lastError) / delay
            modifier = Kp * error + Ki * integral + Kd * derivative
            leftMotor.setPower(basePower + modifier)
            rightMotor.setPower(basePower - modifier)

            lastError = error
            time.sleep(delay)

    def followLine(self, bias = 0):
        self.bias.value = bias
        if ( __name__ == '__main__'):
            if (self.lineFollowProcess == 0):
                self.lineFollowProcess = mlt.Process(target=self.followLineLoop)

class motor:
    direction = 1
    port = 0
    power = 0
    dps = 0
    mmps = 0
    position = 0
    diameter = 2
    degPermm = 1
    mmPerdeg = 1
    BP = 0
    minPower = 0
    maxPower = 100
    def __init__(self, BP, port, reverse = False, diameter = 2, minPower = 0, maxPower = 100):
        self.BP = BP
        self.port = port
        if reverse:
            self.direction = -1
        self.diameter = diameter
        self.minPower = minPower
        self.maxPower = maxPower
        self.degPermm = 360 / math.pi / self.diameter
        self.mmPerdeg = self.diameter * math.pi / 360
    
    def mmdeg(self, millimeters):
        return millimeters * self.degPermm

    def degmm(self, degrees):
        return degrees * self.mmPerdeg
    
    def constrain(val, min_val, max_val):
        return min(max_val, max(min_val, val))
    
    def setPower(self, power):
        try:
            self.BP.set_motor_power(self.port, power)
            self.power = power
        except IOError as error:
            print('error')

    def setPosition(self, position):
        try:
            self.BP.set_motor_position(self.port, position)
            self.position = position
        except IOError as error:
            print('error')

    def setDPS(self, dps):
        try:
            self.BP.set_motor_dps(self.port, dps)
            self.dps = dps
            self.mmps = self.degmm(dps)
        except IOError as error:
            print(error)
    
    def setMMPS(self, mmps):
        try:
            dps = self.mmdeg(mmps)
            self.BP.set_motor_dps(self.port, dps)
            self.mmps = mmps
            self.dps - dps
        except IOError as error:
            print(error)
    
    def rotateDegrees(self, degrees):
        try:
            self.BP.set_motor_position_relative(self.port, degrees)
            self.position = self.BP.get_motor_encoder(self.port)
        except IOError as error:
            print(error)

    def rotateMM(self, millimeters):
        try:
            self.BP.set_motor_position_relative(self.port, self.mmdeg(millimeters))
            self.position = self.BP.get_motor_encoder(self.port)
        except IOError as error:
            print(error)