import sys
import time
import brickpi3
import getConfig
import lineFollowing
from pygame import mixer

mixer.init()
mixer.music.load('WiiChannel.wav')
mixer.music.play()

BP = brickpi3.BrickPi3()
ports = getConfig.getPorts(BP)
LF = lineFollowing.lineFollower(BP, ports)
time.sleep(5)

mixer.music.load('Title.wav')
mixer.music.play()

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

mixer.music.load('Menu.wav')
mixer.music.play()

LF.restart()

mixer.music.load('Countdown.wav')
mixer.music.play()
while mixer.music.get_busy():
    continue
mixer.music.load('CoconutMall.wav')
mixer.music.play()

# for i in range(location):
#     time.sleep(0.5)
#    LF.followLine()
#    LF.straight()
#    time.sleep(1)
#LF.branch()
LF.followLine()
mixer.music.load('FinalLap.wav')
mixer.music.play()
LF.dropOff(cargo)
while mixer.music.get_busy():
    continue

mixer.music.load('FinalCoconutMall.wav')
mixer.music.play()

LF.followLine()
LF.stop()

