import os
import threading
import time
import tkinter.messagebox
from tkinter import *
from tkinter import filedialog

from mutagen.mp3 import MP3
from pygame import mixer

root = Tk()

# Create the menubar
menubar = Menu(root)
root.config(menu=menubar)

# Create the submenu

subMenu = Menu(menubar, tearoff=0)


def browse_file():
    global filename
    filename = filedialog.askopenfilename()


menubar.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="Open", command=browse_file)
subMenu.add_command(label="Exit", command=root.destroy)


def about_us():
    tkinter.messagebox.showinfo('About Melody', 'This is a music MusicPlayer.py build using Python Tkinter by @attreyabhatt')


subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=subMenu)
subMenu.add_command(label="About Us", command=about_us)

mixer.init()  # initializing the mixer

root.title("Melody")
root.iconbitmap(r'images/melody.ico')

filelabel = Label(root, text='Lets make some noise!')
filelabel.pack()

lengthlabel = Label(root, text='Total Length : --:--')
lengthlabel.pack(pady=5)

currenttimelabel = Label(root, text='Current Time : --:--', relief=GROOVE)
currenttimelabel.pack()


def show_details():
    filelabel['text'] = "Playing" + ' - ' + os.path.basename(filename)

    file_data = os.path.splitext(filename)

    if file_data[1] == '.mp3':
        audio = MP3(filename)
        total_length = audio.info.length
    else:
        a = mixer.Sound(filename)
        total_length = a.get_length()

    # div - total_length/60, mod - total_length % 60
    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    lengthlabel['text'] = "Total Length" + ' - ' + timeformat

    t1 = threading.Thread(target=start_count, args=(total_length,))
    t1.start()


def start_count(t):
    global paused
    # mixer.music.get_busy(): - Returns FALSE when we press the stop button (music stop playing)
    # Continue - Ignores all of the statements below it. We check if music is paused or not.
    current_time = 0
    while current_time <= t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(current_time, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            currenttimelabel['text'] = "Current Time" + ' - ' + timeformat
            time.sleep(1)
            current_time += 1


def play_music():
    global paused

    if paused:
        mixer.music.unpause()
        statusbar['text'] = "Music Resumed"
        paused = FALSE
    else:
        try:
            mixer.music.load(filename)
            mixer.music.play()
            statusbar['text'] = "Playing music" + ' - ' + os.path.basename(filename)
            show_details()
        except:
            tkinter.messagebox.showerror('File not found', 'Melody could not find the file. Please check again.')


def stop_music():
    mixer.music.stop()
    statusbar['text'] = "Music Stopped"


paused = FALSE


def pause_music():
    global paused
    paused = TRUE
    mixer.music.pause()
    statusbar['text'] = "Music Paused"


def rewind_music():
    play_music()
    statusbar['text'] = "Music Rewinded"


def set_vol(val):
    volume = int(val) / 100
    mixer.music.set_volume(volume)
    # set_volume of mixer takes value only from 0 to 1. Example - 0, 0.1,0.55,0.54.0.99,1


muted = FALSE


def mute_music():
    global muted
    if muted:  # Unmute the music
        mixer.music.set_volume(0.7)
        volumeBtn.configure(image=volumePhoto)
        scale.set(70)
        muted = FALSE
    else:  # mute the music
        mixer.music.set_volume(0)
        volumeBtn.configure(image=mutePhoto)
        scale.set(0)
        muted = TRUE


middleframe = Frame(root)
middleframe.pack(pady=30, padx=30)

playPhoto = PhotoImage(file='images/play.png')
playBtn = Button(middleframe, image=playPhoto, command=play_music)
playBtn.grid(row=0, column=0, padx=10)

stopPhoto = PhotoImage(file='images/stop.png')
stopBtn = Button(middleframe, image=stopPhoto, command=stop_music)
stopBtn.grid(row=0, column=1, padx=10)

pausePhoto = PhotoImage(file='images/pause.png')
pauseBtn = Button(middleframe, image=pausePhoto, command=pause_music)
pauseBtn.grid(row=0, column=2, padx=10)

# Bottom Frame for volume, rewind, mute etc.

bottomframe = Frame(root)
bottomframe.pack()

rewindPhoto = PhotoImage(file='images/rewind.png')
rewindBtn = Button(bottomframe, image=rewindPhoto, command=rewind_music)
rewindBtn.grid(row=0, column=0)

mutePhoto = PhotoImage(file='images/mute.png')
volumePhoto = PhotoImage(file='images/volume.png')
volumeBtn = Button(bottomframe, image=volumePhoto, command=mute_music)
volumeBtn.grid(row=0, column=1)

scale = Scale(bottomframe, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
scale.set(70)  # implement the default value of scale when music MusicPlayer.py starts
mixer.music.set_volume(0.7)
scale.grid(row=0, column=2, pady=15, padx=30)

statusbar = Label(root, text="Welcome to Melody", relief=SUNKEN, anchor=W)
statusbar.pack(side=BOTTOM, fill=X)


def on_closing():
    stop_music()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
