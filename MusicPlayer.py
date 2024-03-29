## Importing all the neccesary modules.
from pygame import mixer
from mutagen.mp3 import MP3
import os
import vlc
import time

from tkinter import *
import random
import time

#tk = Tk()
#tk.title = "Game"
#tk.resizable(0,0)
#tk.wm_attributes("-topmost", 1)

#canvas = Canvas(tk, width=500, height=400, bd=0, highlightthickness=0)
#canvas.pack()

class Teste:
    def __init__(self):
        self.soundFile = vlc.MediaPlayer('api/TESTE4.mp3')
        #print( self.soundFile.get_length() )
        #print(self.soundFile.get_time())
        #print(self.soundFile.get_title())
        #self.soundFile.audio_set_volume(20)

    def setPosition(self, pos):
        return self.soundFile.set_position(pos)

    def getPosition(self):
        return self.soundFile.get_position()

    def getLength(self):
        return self.soundFile.get_length()

    def getTime(self):
        return self.soundFile.get_time()

    def setRate(self, rate):
        print(rate)
        self.soundFile.set_rate(rate)

    def setVolume(self, db):
        self.soundFile.audio_set_volume(db)

    def changeSample(self, name):
        self.soundFile.stop()
        self.soundFile = vlc.MediaPlayer(name)

    def isPlaying(self):
        return self.soundFile.is_playing()

    def playSampleOld(self):
        print(self.soundFile.is_playing())
        if self.soundFile.is_playing():
            self.soundFile.pause()
            self.is_paused = True
            print('PAUSE get pos', self.soundFile.get_position())
            print('PAUSE get lenght', self.soundFile.get_length())
            print('PAUSE get time', self.soundFile.get_time())
            print('Pause')
        #elif self.soundFile.MediaPlayerEndReached():
        #    print('Acabou')
        else:
            print('Play get position play', self.soundFile.get_position())
            print('Play get lenght', self.soundFile.get_length())
            self.is_paused = False
            if self.soundFile.get_position() > 0.8 and self.soundFile.get_length() < 4000:
                self.soundFile.stop()
            elif self.soundFile.get_position() > 0.85 and self.soundFile.get_length() < 5000:
                self.soundFile.stop()
            elif self.soundFile.get_position() > 0.90 and self.soundFile.get_length() < 6000:
                self.soundFile.stop()
            elif self.soundFile.get_position() > 0.92 and self.soundFile.get_length() < 7000:
                self.soundFile.stop()
            elif self.soundFile.get_position() > 0.95 and self.soundFile.get_length() < 8000:
                self.soundFile.stop()
            elif self.soundFile.get_position() > 0.97 and self.soundFile.get_length() < 9000:
                self.soundFile.stop()
            self.soundFile.play()
            print('Play Get time ', self.soundFile.get_time())

        return self.is_paused
        #self.soundFile.stop()
        #self.soundFile.play()

    def playSample(self):
        self.soundFile.stop()
        self.soundFile.play()

    def pauseSample(self):
        self.soundFile.pause()

    def stopSample(self):
        self.soundFile.stop()


class Ball:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = canvas.create_oval(10, 10, 25, 25, fill=color)
        self.canvas.move(self.id, 245, 100)
        Button(self.canvas, text="Star", width=12, command=self.playSample).pack()
        Button(self.canvas, text="Pause", width=12, command=self.pauseSample).pack()
        Button(self.canvas, text="Stop", width=12, command=self.stopSample).pack()
        self.soundFile = vlc.MediaPlayer('api/TESTE2.wav')

    def playSample(self):


        self.soundFile.play()

    def pauseSample(self):

        self.soundFile.pause()

    def stopSample(self):
        self.soundFile.pause()

    def draw(self):
        pass

#ball = Ball(canvas, "red")

#tk.mainloop()

## Main Class
class Main_class():

    def __init__(self):
        mixer.init()
        mixer.pre_init(44100, 16, 2, 4096)  # frequency, size, channels, buffersize


    def fixString(self, string):
        return ''

    def playSample(self):
        #mixer.music.load('/Users/luisclaudio/Downloads/KF - HTT - Hybrid Hit 1 - Full.wav')
        #mixer.music.load('/Users/luisclaudio/Downloads/KF - HTT - Hybrid Hit 1 - Full.wav')
        #mixer.Sound('/Users/luisclaudio/Downloads/KF - HTT - Hybrid Hit 1 - Full.wav&')
        #mixer.music.play(-1)
        soundFile = vlc.MediaPlayer('api/TESTE2.wav', '--loop')
        #soundFile.set_rate(0.5)
        soundFile.play()
        print(soundFile.is_playing())
        time.sleep(3)
        soundFile.play()
        time.sleep(1)
        #print(soundFile.get_time())
        soundFile.set_time(100)

        soundFile.pause()
        soundFile.stop()
        print(soundFile.is_playing())
        time.sleep(3)

        #soundFile
        #os.system("afplay api/TESTE.wav  &")
        #os.system("afplay api/TESTE2.wav &")
        #os.system("afplay api/TESTE.wav -h &")

    def stopSample(self):
        os.system("afplay api/TESTE.wav -h &")



#music_player = Main_class()
#music_player.playSample()


