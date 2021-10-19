import brickpi3
from getConfig import *

BP = brickpi3.BrickPi3()
ports = getPorts(BP)

input("Move the latch and cable motors into the open position, and press Enter")
BP.reset_motor_encoder(ports['cable motor'])
BP.reset_motor_encoder(ports['latch motor'])
