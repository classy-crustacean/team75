import sys
import brickpi3
sys.path.append(sys.path[0] + "/../..")
import getConfig
import lineFollowing
import time
from pygame import mixer

mixer.init()
mixer.music.load('WiiChannel.wav')
mixer.music.play()
BP = brickpi3.BrickPi3()

ports = getConfig.getPorts(BP)

LF = lineFollowing.lineFollower(BP, ports)
time.sleep(5)

mixer.music.stop()
mixer.music.load('Title.wav')
mixer.music.play()

LF.restart()

mixer.music.stop()
mixer.music.load('Countdown.wav')
mixer.music.play()
while mixer.music.get_busy():
    continue
mixer.music.load('MarioCircuit.wav')
mixer.music.play(loops = -1)

LF.followLine()

LF.stop()
