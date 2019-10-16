from tkinter import *
from tkinter import ttk
import tkinter as tk

class SampleInfo:

    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master, width=400, height=400)

        nameLabel = Label(self.frame, text="Name:")
        nameLabel.grid(row=0, column=0, columnspan=1)

        nameSample = Label(self.frame, text="Teste nome do sample")
        nameSample.grid(row=0, column=1, columnspan=6)

        aa = Label(self.frame, text="Name:")
        aa.grid(row=1, column=0, columnspan=1)

        bb = Label(self.frame, text="Name:")
        bb.grid(row=2, column=0, columnspan=1)

        cc = Label(self.frame, text="Name:")
        cc.grid(row=3, column=0, columnspan=1)

        dd = Label(self.frame, text="Name:")
        dd.grid(row=4, column=0, columnspan=1)

        ee = Label(self.frame, text="Name:")
        ee.grid(row=5, column=0, columnspan=1)

        self.frame.pack()
        Pack()

    def close_windows(self):
        self.master.destroy()