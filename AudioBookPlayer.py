import pygame #used to create video games
import os #it permits to interact with the operating system

pygame.init()
pygame.mixer.init()

class Player:
    
    __version__ = 'v1.0'

    def __init__(self, song_list):
        print("player init")
        if (len(song_list) < 0):
            raise FileNotFoundError("No audio files given!")

        self.currFile = song_list[0]
        self.currDirectory, self.currName = os.path.split(self.currFile)
        self.currName, _ = os.path.splitext(self.currName)
        self._saveFile = os.path.join(self.currDirectory, self.currName + '.abp')
        self.startTime = 0.0
        self.isStarted = False

        if os.path.exists(self._saveFile):
            self._loadSaveFile()

        pygame.mixer.music.load(self.currFile)

    def _loadSaveFile(self):
        with open(self._saveFile) as f:
            version = f.readline().strip('\n')
            if version != self.__version__:
                raise RuntimeError("Version of Save File not known")
            self.startTime = float(f.readline())
            print("Found Start Time: " + str(self.startTime))

    def _updateSaveFile(self, nextStartTime):
        with open(self._saveFile, 'w') as f:
            print(self.__version__, file=f)            
            print(str(nextStartTime), file=f)

    def Play(self):
        print("player play")
        if (not self.isStarted):
            pygame.mixer.music.play(start=self.startTime)
            self.isStarted = True
        else:
            pygame.mixer.music.unpause()

    def Pause(self):
        print("player pause")
        pygame.mixer.music.pause()
        currTime = self.startTime + float(pygame.mixer.music.get_pos()) /1000 
        self._updateSaveFile(currTime)
