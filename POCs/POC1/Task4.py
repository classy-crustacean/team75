import sys
import brickpi3
sys.path.append(sys.path[0] + "/../..")
import getConfig
import lineFollowing

BP = brickpi3.BrickPi3()

ports = getConfig.getPorts(BP)

LF = lineFollowing.lineFollower(BP, ports)

LF.followLine()
