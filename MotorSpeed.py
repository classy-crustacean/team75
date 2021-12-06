#this code was taken from the BrickPi

#https://www.dexterindustries.com/BrickPi/
#https://github.com/DexterInd/BrickPi3
#
#Copyright (c) 2016 Dexter Industries
#Released under the MIT liscence (https://choosealiscence.com/liscences/mit/)
#For more information, see https://github/DexterInd/BrickPi3/blob/master/LISCENCE.md

#This code converts an input speed in centimeters per second to motor rotational speed in degrees per second - zrramire


import time
import brickpi3
import math
BP = brickpi3.BrickPi3()

target = (float(input("State the desired speed in cm/s: ")) * 360 * 40) / (24 * 6.8 * math.pi)
distance = (float(input("State the desired distance in cm: ")) * 360 * 40) / (24 * 6.8 * math.pi)
#Converts the input speed to degrees per second using the circumference and rad/sec to degree/sec conversion - zrramire

try:
    try:
        BP.offset_motor_encoder(BP.PORT_A, BP.get_motor_encoder(BP.PORT_A))
        BP.offset_motor_encoder(BP.PORT_D, BP.get_motor_encoder(BP.PORT_D))
        #BP.set_motor_power(BP.PORT_A, BP.MOTOR_FLOAT)
        #BP.set_motor_power(BP.PORT_D, BP.MOTOR_FLOAT)
    
    except IOError as error:
        print(error)

    degs = 0
    while (degs < distance):
        BP.set_motor_dps(BP.PORT_A, target)
        BP.set_motor_dps(BP.PORT_D, target)
        time.sleep(0.05)
        degs = BP.get_motor_encoder(BP.PORT_A)
        print(degs)
    BP.set_motor_dps(BP.PORT_A, 0)
    BP.set_motor_dps(BP.PORT_D, 0)
      
    time.sleep(0.5)
    BP.reset_all()
except KeyboardInterrupt:
    BP.reset_all()
