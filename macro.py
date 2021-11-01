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
    goal = 64
    bias = mlt.Value('i', 0)
    lastPosition = mlt.Value('d', 0)
    lineSensors = []
    def __init__(self, BP, config):
        self.config = config
        self.rightMotor = Motor(BP, config['right drive motor'], diameter=config['rear wheel diameter'])
        self.leftMotor = Motor(BP, config['left drive motor'], diameter=config['rear wheel diameter'])
        self.frontMotor = Motor(BP, config['front drive motor'], diameter=config['front wheel diameter'])
        maxLineValue = self.config['max line value']

        maxPosition = 0
        for i in range(len(self.config['color line sensors'])):
            port = self.config['color line sensors'][i]
            position = self.config['color line sensor positions'][i]
            self.lineSensors.append(ColorLineSensor(BP, port, position, maxLineValue)) 
            if (position > maxPosition):
                maxPosition = position
        for i in range(len(self.config['line finders'])):
            port = self.config['line finders'][i]
            position = self.config['line finder positions'][i]
            self.lineSensors.append(LineFinder(port, position, maxLineValue))
            if (position > maxPosition):
                maxPosition = position

        self.goal = maxPosition / 2
        
    
    # I based a lot of my position code on http://robotresearchlab.com/2019/03/13/build-a-custom-pid-line-following-robot-from-scratch/#Programming_the_motors
    def getPositionUnbiased(self, lastPosition):
        sensors = self.readLineSensors()
        num = 0
        sum = 0
        for sensor in self.lineSensors:
            read = sensor.readLine()
            num += read['value'] * read['position']
            sum += read['value']
        
        if (num > 32):
            lastPosition = sum / num
        
        return lastPosition
    
    def getPositionRightBias(self, lastPosition):
        raise NotImplementedError("implement right bias dumbass")
        num = 0
        sum = 0
        for sensor in self.lineSensors:
            read = sensor.readLine()
        
        if (num != 0):
            lastPosition = sum / num
        
        return lastPosition

    def getPositionLeftBias(self, lastPosition):
        raise NotImplementedError("implement left bias dumbass")
        values = self.readLineFinders
        num = 0
        sum = 0
        for i in reversed(range(0, len(values))):
            value = values[i]
            if (value == 1):
                if (i < self.goal and num > 0):
                    if (sum / num > self.goal):
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
        basePower = self.config['base motor power']
        leftMotor = self.leftMotor
        rightMotor = self.rightMotor

        position = 0
        error = 0
        lastError = 0
        integral = 0
        derivative = 0
        delay = 0.02
        while True:
            if (self.bias.value == 0):
                position = self.getPositionUnbiased(position)
            elif (self.bias.value == 1):
                position = self.getPositionLeftBias(position)
            elif (self.bias.value == 2):
                position = self.getPositionRightBias(position)
            error = self.goal - position
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

class Motor:
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
        self.port = {'A': BP.PORT_A,
                     'B': BP.PORT_B,
                     'C': BP.PORT_C,
                     'D': BP.PORT_D}[port]
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

# Template class for all sensor classes
class Sensor:
    def getValue(self, maxValue):
        raise NotImplementedError(f"Please implement getValue in {type(self)}")

# Template class for all LEGO sensors
class LEGOSensor(Sensor):
    port = None
    BP = None

    def __init__(self, BP, port):
        self.BP = BP
        self.port = {1: BP.PORT_1,
                     2: BP.PORT_2,
                     3: BP.PORT_3,
                     4: BP.PORT_4}[port]

# Template class for all grove sensors
class GroveSensor(Sensor):
    port = None
    
    def __init__(self, port):
        self.port = port

# Template class for all sensors that are used to detect lines
class LineSensor(Sensor):
    position = None
    maxValue = None
    def __init__(self, position, maxValue):
        self.position = position
        self.maxValue = maxValue
    
    def getLineValue(self):
        raise NotImplementedError(f"Please implement getLineValue in {type(self)}")
    
    def readLine(self):
        return {'value': self.getLineValue(), 'position': self.position}


# Class for LEGO touch sensors
class touchSensor(LEGOSensor):
    def __init__(self, BP, port):
        super().__init__(BP, port)
        try:
            self.BP.set_sensor_type(self.port, self.BP.SENSOR_TYPE.TOUCH)
            time.sleep(0.02)
        except brickpi3.SensorError:
            print(f"Configuring touch sensor in port {self.port}")
            error = True
            while error:
                time.sleep(0.05)
                try:
                    self.BP.get_sensor(self.port)
                    error = False
                except brickpi3.SensorError:
                    error = True
    
    def getValue(self):
        try:
            return self.BP.get_sensor(self.port)
        except IOError as error:
            print(f"Error reading from touch sensor in port {self.port}")
            print(error)

# Class for LEGO color sensor used to find line
class ColorLineSensor(LEGOSensor, LineSensor):
    def __init__(self, BP, port, position, maxValue):
        super(LEGOSensor, self).__init__(BP, port)
        super(LineSensor, self).__init__(position, maxValue)
        try:
            self.BP.set_sensor_type(self.port, self.BP.SENSOR_TYPE.EV3_COLOR_REFLECTED)
            time.sleep(0.02)
        except brickpi3.SensorError:
            print(f"Configuring color sensor in port {self.port}")
            error = True
            while error:
                time.sleep(0.05)
                try:
                    self.BP.get_sensor(self.port)
                    error = False
                except brickpi3.SensorError:
                    error = True
        
    def getValue(self):
        try:
            return self.BP.get_sensor(self.port)
        except brickpi3.SensorError as error:
            print(f"Error reading value of color sensor in port {self.port}")
            print(error)
    
    def getLineValue(self):
        # inverts the reading, so a line is a high value
        return self.maxValue - self.getValue()

# Class for grove line finders used to find line
class LineFinder(GroveSensor, LineSensor):
    def __init__(self, port, position, maxValue):
        super(GroveSensor, self).__init__(port)
        super(LineSensor, self).__init__(position, maxValue)
    
    def getValue(self):
        try:
            return grovepi.digitalRead(self.port)
        except IOError as error:
            print(f"Error reading value of line finder in port D{self.port}")
            print(error)
    
    def getLineValue(self):
        # returns the max value instead of a 1 to match the color sensors
        return self.getValue() * self.maxValue
    