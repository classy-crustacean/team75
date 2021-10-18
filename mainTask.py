import time
from brickpi3 import *
from getConfig import *
from lineFollowing import *

BP = BrickPi3()
ports = getPorts(BP)

LF = lineFollower(BP, ports)

targets = [1,2,3]

for target in targets:
    for i in range(0,target):
        time.sleep(0.5)
        LF.followLine()
    LF.branch()
    LF.followLine()
    LF.dropOff()
    LF.followLine()
    LF.restart()
