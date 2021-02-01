""" 
Audiobook player
Designed to make playing audiobooks as comfortable as possible
Player features inspired from: https://towardsdatascience.com/how-to-build-an-mp3-music-player-with-python-619e0c0dcee2
"""

import pygame #used to create video games
import tkinter as tk #used to develop GUI
from tkinter.filedialog import askdirectory #it permit to select dir
import os #it permits to interact with the operating system

pygame.init()
pygame.mixer.init()

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.master.title('Andi\'s Audio Book Player') 
        self.master.geometry('450x350')
        self.create_menubar()
        self.create_widgets()

    def create_menubar(self):
        menubar = tk.Menu(self)
        menubar.add_command(label="Select Files", command=self.SelectFiles)  
        menubar.add_command(label="Close", command=self.Close)  
        self.master.config(menu=menubar)

    def create_widgets(self):
        pass
        self.title = self.titleLabel = tk.Label(self.master, text = 'Audiobook Player', bg='black', fg='red')
        self.titleLabel.pack(side='top', fill='x', expand=1)

    def SelectFiles(self):
        print("Do Do...")

    def Close(self):
        print("Done...")
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()