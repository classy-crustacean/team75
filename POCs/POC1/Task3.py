import sys
import time
import brickpi3
sys.path.append(sys.path[0] + "/../..")
import getConfig
import lineFollowing

BP = brickpi3.BrickPi3()
ports = getConfig.getPorts(BP)
LF = lineFollowing.lineFollower(BP, ports)

location = int(input("""
Choose Location:
    1: Point A
    2: Point B
    3: Point c

Enter Location Choice: """))

cargo = int(input("""
Choose Cargo Type:
    1: Habitat Cargo (Cylinder)
    2: Water Harvester (Rectangle)
    3: Power Generation Unit (Cone)

Enter Cargo Choice: """))

LF.restart()
for i in range(location):
    time.sleep(0.5)
    LF.followLine()
LF.branch()
LF.followLine()
LF.dropOff()
LF.followLine()
