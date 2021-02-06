""" 
Audiobook player
Designed to make playing audiobooks as comfortable as possible
Player features inspired from: https://towardsdatascience.com/how-to-build-an-mp3-music-player-with-python-619e0c0dcee2
"""

import pygame #used to create video games
import tkinter as tk #used to develop GUI
import tkinter.filedialog as tkfile
import fontawesome as fa
import os #it permits to interact with the operating system
from pynput.keyboard import Listener
from AudioBookPlayer import Player
import threading
import time

BG_COLOR='gray12'
FG_COLOR='wheat3'

def Sec2HMinSec(timeSec: float):
    H = int((timeSec // 60) // 60)
    m = int(timeSec // 60 - 60 * H)
    sec = int(timeSec - 60*m - 60*60*H)

    return H, m, sec

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.master.title('Andi\'s Audio Book Player') 
        self.master.geometry('450x350')
        self.master['bg'] = BG_COLOR
        self.create_menubar()
        self.create_title()
        # self.create_widgets()

    def create_menubar(self):
        menubar = tk.Menu(self)
        menubar.add_command(label="Select Files", command=self.SelectFiles)  
        menubar.add_command(label="Close", command=self.Close)  
        self.master.config(menu=menubar)

    def create_title(self):
        self.titleLabel = tk.Label(self.master, text = 'Audiobook Player',fg=FG_COLOR, bg=BG_COLOR, font=("Consolas", 22))
        self.titleLabel.pack(side='top', fill='x', expand=1)

    def create_widgets(self, player):
        nameLabel = tk.Label(self.master, text = 'Playing: ' + player.currName, fg=FG_COLOR, bg=BG_COLOR, font=("Consolas", 14))
        nameLabel.pack(side='top', fill='x', expand=1)
        PlayButton = tk.Button(self.master, text='Play', command=player.Play, fg='wheat1', bg='black', font=("Consolas", 10))
        PlayButton.pack(side='top', fill='x', expand=1)
        PauseButton = tk.Button(self.master, text='Pause', command=player.Pause, fg='wheat1', bg='black', font=("Consolas", 10))
        PauseButton.pack(side='top', fill='x', expand=1)
        PausePlayButton = tk.Button(self.master, text='Pause / Play', command=player.PausePlay, fg='wheat1', bg='black', font=("Consolas", 16))
        PausePlayButton.pack(side='top', fill='x', expand=1)
        self.TimeLable = tk.Label(self.master, text = '00:00:00  /  00:00:00', fg=FG_COLOR, bg=BG_COLOR, font=("Consolas", 12))
        self.TimeLable.pack(side='top', fill='x', expand=1)
        
        listener_thread = Listener(on_press=self.on_press, on_release=None)
        # This is a daemon=True thread, use .join() to prevent code from exiting  
        listener_thread.start()

        timeUpdateThread = threading.Thread(target=self.updateTime)
        timeUpdateThread.daemon = True
        timeUpdateThread.start()

    def SelectFiles(self):
        # currently not used option to select a whole directory
        # directory = tk.filedialog.askdirectory()
        # os.chdir(directory)
        # song_list = os.listdir()
        song =  tk.filedialog.askopenfilename(title='Select Audio File...')
        song_list = []
        if len(song) > 0:
            song_list = [song] # only handle single files for now
        print(song_list)
        if len(song_list) > 0:
            self.bookPlayer = Player(song_list)
            self.create_widgets(self.bookPlayer)

    def Close(self):
        print("Done...")
        try:
            if self.bookPlayer is not None:
                self.bookPlayer.Pause()
        except AttributeError:
            pass # closing without player initialized 
        self.master.destroy()

    def root_on_press(self, event):
        keyChar = None
        try:
            keyChar = event.char
        except AttributeError:
            keyChar = str(event)

        if keyChar == ' ':
            self.bookPlayer.PausePlay()


    def updateTime(self):
        while (True):
            currTime = self.bookPlayer.GetCurrentTime()
            cH, cMin, cSec = Sec2HMinSec(currTime)
            maxTime = self.bookPlayer.AudioLengthTime
            maxH, maxMin, maxSec = Sec2HMinSec(maxTime)
            self.TimeLable['text'] = '{:02d}:{:02d}:{:02d}  /  {:02d}:{:02d}:{:02d}'.format(cH, cMin, cSec, maxH, maxMin, maxSec)
            time.sleep(1.0)

    def on_press(self, key):
        try:
            val = str(key.value)
        except AttributeError:
            val = str(key)
        if val == '<179>':
            # play pause media key was pressed
            self.bookPlayer.PausePlay()
        if val == '<176>':
            # next key was pressed
            self.bookPlayer.StepForward()
        if val == '<177>':
            # previous key was pressed
            self.bookPlayer.StepBack()

    def on_release(self, key):
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    root.protocol("WM_DELETE_WINDOW", app.Close)
    root.bind('<KeyPress>', app.root_on_press)
    app.mainloop()