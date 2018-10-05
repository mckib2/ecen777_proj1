import tkinter as tk
from tkinter import ttk
from proj1 import load_ogg,synthesize_vowel,save
from contextlib import contextmanager
import sys,os
import numpy as np

# Supress messages on module load
@contextmanager
def suppress_stdout():
    with open(os.devnull,'w') as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout
with suppress_stdout():
    import pygame as pg

class Application(tk.Frame):
    def __init__(self,master=None):
        super().__init__(master)
        self.pack()

        # Load the sound files, initialize the mixer
        self.data,self.samplerate = load_ogg()
        pg.mixer.init(self.samplerate)

        # Build the form elements
        self.create_widgets()

    def create_widgets(self):

        # # Display sample rate
        # self.samplerate_label = tk.Label(self,text='Sample rate is %d' % self.samplerate)
        # self.samplerate_label.pack()

        # Choose vowel sound
        self.vowel_label = tk.Label(self,text='Select Vowel Sound:').pack()
        self.vowel_select = ttk.Combobox(self)
        self.vowel_select['text'] = 'select'
        self.vowel_select['values'] = list(self.data.keys())
        self.vowel_select.bind("<<ComboboxSelected>>",lambda ev: self.play_vowel(ev))
        self.vowel_select.pack(side="top")

        # Choose pitch
        self.freq_label = tk.Label(self,text='Desired frequency (Hz):').pack()
        self.freq_entry = tk.Entry(self)
        self.freq_entry.insert(0,'200')
        self.freq_entry.pack()

        # Choose a duration to play the vowel
        self.duration_label = tk.Label(self,text='Desired duration of playback (sec):').pack()
        self.duration_entry = tk.Entry(self)
        self.duration_entry.insert(0,'1.5')
        self.duration_entry.pack()

        # Quit
        self.quit = tk.Button(self,text="QUIT",fg="red",command=root.destroy)
        self.quit.pack(side="bottom")

    def play_vowel(self,ev):
        # Stop any sounds that might be playing already
        pg.mixer.stop()

        # Get the desired vowel
        vowel = self.vowel_select.get()

        # Get the desired frequency
        freq = int(self.freq_entry.get())

        # Get the desired playback length
        dur = float(self.duration_entry.get())

        # Do the thing
        synth,samplerate0 = synthesize_vowel(self.data,vowel,freq=freq,duration=dur,samplerate=self.samplerate)

        # Save the result, then play it
        filename = save('%s_synth.ogg' % vowel,synth,samplerate=samplerate0)
        pg.mixer.Sound(filename).play()


root = tk.Tk()
root.title('ECEn 777 - Project 1')
app = Application(master=root)
app.mainloop()
