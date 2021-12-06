from MPU9250 import MPU9250
import brickpi3
import grovepi
import time
import math
import numpy as np
import multiprocessing as mlt
from MCP3008 import MCP3008

class MACRO:
    config = None
    rightMotor = None
    leftMotor = None
    latchMotor = None
    lineFollowProcess = None
    goal = None
    bias = mlt.Value('i', 0)
    lineSensors = []
    threshold = None
    mcp = None
    BP = None
    numLines = mlt.Value('i', 0)
    imu = None

    def __init__(self, BP, config):
        self.config = config
        self.rightMotor = Motor(BP, config['right drive motor'], diameter=config['rear wheel diameter'], gearRatio=config['rear wheel gear ratio'])
        self.leftMotor = Motor(BP, config['left drive motor'], diameter=config['rear wheel diameter'], gearRatio=config['rear wheel gear ratio'])
        self.latchMotor = Motor(BP, config['latch motor'], diameter=config['dia pitch latch gear'], reverse = True)
        #self.ultrasonic = EV3Ultrasonic(BP, config['ultrasonic sensor'])
        self.threshold = config['threshold']

        self.mcp = initMCP(0, 0)

        self.initLineSensors()
        self.BP = BP
        try:
            self.imu = IMU_Magnet()
        except IOError:
            print("There is no IMU connected")

    
    
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
        if (portsLF != None and portsIR != None):
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

        elif (portsIR != None):
            while (ir < len(portsIR)):
                sensors.append(IRSensor(self.mcp, portsIR[ir], posIR[ir], maxValue))
                maxPosition = posIR[ir]
                ir += 1
        elif (portsLF != None):
            while (lf < len(portsLF)):
                sensors.append(LineFinder(portsLF[lf], posLF[lf], maxValue))
                maxPosition = posLF[lf]
                lf += 1
        self.goal = maxPosition / 2
        self.lineSensors = sensors

        
    # I based a lot of my position code on http://robotresearchlab.com/2019/03/13/build-a-custom-pid-line-following-robot-from-scratch/#Programming_the_motors
    def getLinePositions(self, readings):
        lines = []
        num = 0
        sum = 0
        for read in readings:
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

        if (sum != 0):
            lines.append(num / sum)
        
        self.numLines.value = len(lines)
        print(lines)
        return lines
    
    # I based a lot of my position code on http://robotresearchlab.com/2019/03/13/build-a-custom-pid-line-following-robot-from-scratch/#Programming_the_motors
    def getLinePositionUnbiased(self, readings):
        num = 0
        sum = 0
        for read in readings:
            # Add values to num and sum when sensor is above threshold
            if (read['value'] > self.threshold):
                num += read['value'] * read['position']
                sum += read['value']
        if (sum != 0):
            return num / sum
        else:
            return None

    def getLineReadings(self):
        readings = []

        for sensor in self.lineSensors:
            read = sensor.readLine()
            if (read['value'] > self.threshold):
                readings.append(read)
        return readings

    def followLineLoop(self):
        Kp = self.config['Kp']
        Ki = self.config['Ki']
        Kd = self.config['Kd']
        baseSpeed = self.config['base motor speed']
        speedChange = self.config['speed change']
        leftMotor = self.leftMotor
        rightMotor = self.rightMotor

        position = 0
        error = 0
        lastError = 0
        integral = 0
        derivative = 0
        delay = 0.05
        speedIncrease = 0
        while True:
            readings = self.getLineReadings()
            if (self.bias.value == -1):
                linePosition = self.getLinePositionUnbiased(readings)
                if (linePosition != None):
                    position = linePosition
            elif (self.bias.value == 0):
                linePosition = self.getLinePositionUnbiased(readings)
                if (linePosition != None):
                    position = linePosition - 3
            elif (self.bias.value == 1):
                linePosition = self.getLinePositionUnbiased(readings)
                if (linePosition != None):
                    position = linePosition + 3
            error = self.goal - position
            integral = integral + error * delay
            derivative = (error - lastError) / delay
            modifier = Kp * error + Ki * integral + Kd * derivative
            if (abs(error) < 2):
                speedIncrease = speedChange
            else:
                speedIncrease = 0
            leftMotor.setDPS(baseSpeed - modifier + speedIncrease)
            rightMotor.setDPS(baseSpeed + modifier + speedIncrease)

            lastError = error
            time.sleep(delay)

    def followLine(self, bias = -1):
        self.bias.value = bias
        print(self.lineFollowProcess)
        if (self.lineFollowProcess == None):
            self.lineFollowProcess = mlt.Process(target=self.followLineLoop)
            self.lineFollowProcess.start()
    
    def setBias(self, bias):
        self.bias.value = bias
        print("bias:", bias)

    def stop(self):
        if (self.lineFollowProcess != None):
            self.lineFollowProcess.terminate()
            self.lineFollowProcess.join()
            self.lineFollowProcess = None
        self.leftMotor.setDPS(0)
        self.rightMotor.setDPS(0)

    def terminate(self):
        if (self.lineFollowProcess != None):
            self.lineFollowProcess.terminate()
            self.lineFollowProcess.join()
            self.lineFollowProcess = None
        self.BP.reset_all()
    
    def dropCargo(self):
        self.latchMotor.setDPS(600)
        time.sleep(1)
        self.latchMotor.setDPS(0)
        self.latchMotor.float()
    
    def reset(self):
        self.latchMotor.float()
    
    def driveForward(self, speed, distance):
        dps = (speed * 360 * self.config['rear wheel gear ratio']) / (self.config['rear wheel diameter'] * math.pi)
        degs = (distance * 360 * self.config['rear wheel gear ratio']) / (self.config['rear wheel diameter'] * math.pi)
        self.leftMotor.setDPS(dps)
        self.rightMotor.setDPS(dps)
        while (self.leftMotor.getPosition() < degs):
            time.sleep(0.05)
        self.stop()

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
            self.BP.set_motor_power(self.port, power * self.direction)
            self.power = power
        except IOError as error:
            print('error')

    def setDPS(self, dps):
        print(dps)
        try:
            self.BP.set_motor_dps(self.port, dps * self.direction)
            self.dps = dps
            self.mmps = self.degmm(dps)
        except IOError as error:
            print(error)
    
    def float(self):
        try:
            self.BP.set_motor_power(self.port, self.BP.MOTOR_FLOAT)
        except IOError as error:
            print(error)
    
    def getPosition(self):
        return self.BP.get_motor_encoder(self.port)

def initMCP(bus, chip):
    mcp = MCP3008(bus = 0, device = 0)
    return mcp

# Template class for all sensor classes
class Sensor:
    def getValue(self):
        raise NotImplementedError("Please implement getValue in", type(self))

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
    mcp = None

    def __init__(self, mcp, channel):
        self.channel = channel
        self.mcp = mcp
    
    def getValue(self):
        return(self.mcp.read(channel = self.channel))
        
# Template class for all sensors that are used to detect lines
class LineSensor(Sensor):
    position = None
    maxValue = None
    def __init__(self, position, maxValue):
        self.position = position
        self.maxValue = maxValue
    
    def getLineValue(self):
        raise NotImplementedError("Please implement getLineValue in", type(self))
    
    def readLine(self):
        return {'value': self.getLineValue(), 'position': self.position}
    
class IRSensor(AnalogSensor, LineSensor):
    def __init__(self, mcp, channel, position, maxValue):
        AnalogSensor.__init__(self, mcp, channel)
        LineSensor.__init__(self, position, maxValue)
    
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
            print("Configuring touch sensor in port", self.port)
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
            print("Error reading from touch sensor in port", self.port)
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
            print("Configuring color sensor in port", self.port)
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
            print("Error reading value of color sensor in port", self.port)
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
            print("Error reading value of line finder in port D" + str(self.port))
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
            print("Configuring color sensor in port", self.port)
            error = True
            while error:
                time.sleep(0.05)
                try:
                    self.BP.get_sensor(self.port)
                    error = False
                except brickpi3.SensorError:
                    error = True

class EV3Ultrasonic(LEGOSensor):
    def __init__(self, BP, port):
        super().__init__(BP, port)
        try:
            self.BP.set_sensor_type(self.port, self.BP.SENSOR_TYPE.EV3_ULTRASONIC_CM) # Configure for an EV3 ultrasonic sensor.
            time.sleep(0.02)
        except brickpi3.SensorError:
            print("Configuring EV3 ultrasonic sensor in port", self.port)
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
            print("Error reading from EV3 ultrasonic sensor in port", self.port)
            print(error)

class IMU_Magnet(Sensor):
    mpu = None

    def __init__(self):
        self.mpu = MPU9250()
    
    # returns the distance from the magnet
    def getValue(self):
        mag = self.getXYZ()
        x = mag['x']
        if (mag['z'] < 20):
            x = x * -1
        if (x < 0):
            return math.sqrt(math.pow(mag['x'], 2) + math.pow(mag['y'], 2))
        elif (x > 0):
            return math.sqrt(math.pow(mag['x'], 2) + math.pow(mag['y'], 2)) * -1

    
    # returns the x, y, and z coordinates of the detected magnet
    def getXYZ(self):
        read = self.mpu.readMagnet()
        return read

