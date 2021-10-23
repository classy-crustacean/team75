import sys
import brickpi3
import getConfig
import lineFollowing
from pygame import mixer
import time

mixer.init()
mixer.music.load('WiiChannel.wav')
mixer.music.play()

BP = brickpi3.BrickPi3()

ports = getConfig.getPorts(BP)

LF = lineFollowing.lineFollower(BP, ports)
time.sleep(5)
mixer.music.load('Countdown.wav')
mixer.music.play()
while mixer.music.get_busy():
    continue
mixer.music.load('DKSummit.wav')
mixer.music.play(loops = -1)

LF.followLine()

LF.stop()
