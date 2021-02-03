import pygame #used to create video games
from mutagen.mp3 import MP3
import os #it permits to interact with the operating system

pygame.init()
pygame.mixer.init()

START_MARGIN_S = 10.0
STEP_SIZE = 10.0

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
        self.stepTimeOffset = 0.0
        self.isStarted = False
        self.isPlaying = False

        if os.path.exists(self._saveFile):
            self._loadSaveFile()

        pygame.mixer.music.load(self.currFile)
        song = MP3(self.currFile)
        self.AudioLengthTime = song.info.length

    def _loadSaveFile(self):
        with open(self._saveFile) as f:
            version = f.readline().strip('\n')
            if version != self.__version__:
                raise RuntimeError("Version of Save File not known")
            self.startTime = float(f.readline())
            self.startTime = self.startTime - START_MARGIN_S if self.startTime > START_MARGIN_S else 0.0
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
        self.isPlaying = True

    def Pause(self):
        print("player pause")
        pygame.mixer.music.pause()
        currTime = self.GetCurrentTime()
        self._updateSaveFile(currTime)
        self.isPlaying = False

    def PausePlay(self):
        if self.isPlaying:
            self.Pause()
        else:
            self.Play()

    def GetCurrentTime(self):
        return self.startTime + float(pygame.mixer.music.get_pos()) /1000 + self.stepTimeOffset

    def GetAudioFullTime(self):
        return pygame.mixer.music.get_l

    def StepBack(self):
        print("Player step back")
        currTime = self.GetCurrentTime()
        pygame.mixer.music.set_pos(currTime - STEP_SIZE if currTime > STEP_SIZE else 0.0)
        self.stepTimeOffset -= STEP_SIZE

    def StepForward(self):
        print("Player step forward")
        currTime = self.GetCurrentTime()
        pygame.mixer.music.set_pos(currTime + STEP_SIZE)
        self.stepTimeOffset += STEP_SIZE

