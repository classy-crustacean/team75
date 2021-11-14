import brickpi3
import grovepi
import time
import math
import numpy as np
import multiprocessing as mlt
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

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
    threshold = 0
    mcp = None
    def __init__(self, BP, config):
        self.config = config
        self.rightMotor = Motor(BP, config['right drive motor'], diameter=config['rear wheel diameter'])
        self.leftMotor = Motor(BP, config['left drive motor'], diameter=config['rear wheel diameter'])
        self.frontMotor = Motor(BP, config['front drive motor'], diameter=config['front wheel diameter'])
        self.threshold = config['threshold']

        self.mcp = initMCP(0, 0)

        self.initLineSensors()

    
    
    def initLineSensors(self):
        sensors = []
        maxPosition = 0
        maxValue = 1024
        portsLF = self.config['line finders']
        posLF = self.config['line finder positions']
        portsIR = self.config['ir sensors']
        posIR = self.config['ir positions']
        lf = 0
        ir = 0

        while (lf < len(portsLF) and ir < len(portsIR)):
            if (min(posLF[lf:]) < min(posIR[ir:])):
                sensors.append(LineFinder(portsLF[lf], posLF[lf], maxValue))
                lf += 1
            else:
                sensors.append(IRSensor(self.mcp, portsIR[ir], posIR[ir], maxValue))
                ir += 1
        
        while (lf < len(portsLF) or ir < len(portsIR)):
            if (lf < len(portsLF)):
                sensors.append(LineFinder(portsLF[lf], posLF[lf], maxValue))
                maxPosition = posLF[lf]
                lf += 1
            else:
                sensors.append(IRSensor(self.mcp, portsIR[ir], posIR[ir], maxValue))
                maxPosition = posIR[ir]
                ir += 1

        self.lineSensors = sensors
        self.goal = maxPosition / 2
        
    # I based a lot of my position code on http://robotresearchlab.com/2019/03/13/build-a-custom-pid-line-following-robot-from-scratch/#Programming_the_motors
    def getLinePositions(self):
        lines = []
        num = 0
        sum = 0
        for sensor in self.lineSensors:
            read = sensor.readLine()
            # Add values to num and sum when sensor is above threshold
            if (read['value'] > self.threshold):
                num += read['value'] * read['position']
                sum += read['value']
            # sensor below threshold
            else:
                # if there is a running num and sum, add the average to the lines
                if (sum != 0):
                    lines.append(num / sum)
                # reset num and sum
                num = 0
                sum = 0

        return lines


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
            linePositions = self.getLinePositions()
            if (len(linePositions) != 0):
                if (self.bias.value == 0):
                    position = sum(linePositions) / len(linePositions)
                elif (self.bias.value == 1):
                    position = min(linePositions)
                elif (self.bias.value == 2):
                    position = max(linePositions)
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

def initMCP(bus, chip):
    spiPins = {0: {'clock': board.SCK0,
                   'MOSI': board.MOSI0,
                   'MISO': board.MISO0,
                   'CE': {0: board.CE0, 1: board.CE0_1}},
               1: {'clock': board.SCK1,
                   'MOSI': board.MOSI1,
                   'MISO': board.MISO1,
                   'CE': {0: board.CE1, 1: board.CE1_1}}}
    spi = busio.SPI(clock = spiPins[bus]['clock'], MOSI = spiPins[bus]['MOSI'], MISO = spiPins[bus]['MISO'])
    cs = digitalio.DigitalInOut(spiPins[bus]['CE'][chip])
    mcp = MCP.MCP3008(spi, cs)
    return mcp

# Template class for all sensor classes
class Sensor:
    def getValue(self):
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

class AnalogSensor(Sensor):
    channel = None

    def __init__(self, mcp, channel):
        self.channel = AnalogIn(mcp, channel)
    
    def getValue(self):
        return self.channel.value
        
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
    
class IRSensor(AnalogSensor, LineSensor):
    def __init__(self, mcp, channel, position, maxValue):
        super(AnalogSensor, self).__init__(mcp, channel)
        super(LineSensor, self).__init__(position, maxValue)
    
    def getLineValue(self):
        return self.maxValue - self.getValue()


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
        grovepi.pinMode(port, "INPUT")
    
    def getValue(self):
        try:
            return grovepi.digitalRead(self.port)
        except IOError as error:
            print(f"Error reading value of line finder in port D{self.port}")
            print(error)
    
    def getLineValue(self):
        # returns the max value instead of a 1 to match the color sensors
        return self.getValue() * self.maxValue

class MagnetSensor(GroveSensor):
    def __init__(self, port):
        super().__init__(port)
        grovepi.pinMode(port, "INPUT")
    
    def getValue(self):
        return grovepi.digitalRead(self.port)

class UltrasonicSensor(GroveSensor):
    def __init__(self, port):
        super().__init__(port)
        grovepi.set_bus("RPI_1")
    
    def getValue(self):
        return grovepi.ultrasonicRead(self.port)

class ColorSensor(LEGOSensor):
    def __init__(self, BP, port):
        super().__init__(BP, port)
        try:
            self.BP.set_sensor_type(self.port, self.BP.SENSOR_TYPE.EV3_COLOR_COLOR)
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

