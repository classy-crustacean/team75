import brickpi3
from getConfig import *
from pygame import mixer

mixer.init()
mixer.music.load('ItemBox.wav')
mixer.music.play(-1)

BP = brickpi3.BrickPi3()
ports = getPorts(BP)

mixer.music.load('ItemSelected.wav')
input("Move the latch and cable motors into the open position, and press Enter")
mixer.music.play(0)
BP.reset_motor_encoder(ports['cable motor'])
BP.reset_motor_encoder(ports['latch motor'])

while mixer.music.get_busy():
    continue
