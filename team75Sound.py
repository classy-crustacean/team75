import playsound
from multiprocessing import Process

class soundPlayer:
    def __init__(self):
        self.player = 0
    
    def playMusic(self, file, wait):
        if __name__ == "__main__":
            if self.player != 0:
                self.player.terminate()
            self.player = Process(target=self.repeatSound, args=(file,))
            self.player.start()
            if wait:
                self.player.join()
    
    def playSoundEffect(self, file):
        playsound(file, False)
    
    def repeatSound(file):
        while True:
            playsound(file)
    
    def stopMusic(self):
        if self.player != 0:
            self.player.terminate()
