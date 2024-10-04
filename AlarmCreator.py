import math
import os
from tkinter import *
from tkinter import ttk
from tkinter.ttk import Combobox
from os import path
from Alarm import Alarm


class AlarmCreator:
    sounds_folder = 'Alarms'
    sound_files = ["neraton.mp3"]
    def __init__(self, app, parent=None):
        self.window = Toplevel(parent)
        self.window.title("Alarm Creator")
        self.window.geometry("250x300")
        self.window.resizable(False, False)
        self.label = Label(self.window, text="Add Alarm")
        self.label.grid(column=0, row=0, columnspan=2)
        self.count_label = Label(self.window, text="Ring after counter reaches: ")
        self.count_label.grid(column=0, row=1, columnspan=2)

        self.count_var = IntVar(self.window, value=0)

        self.count_dial = Spinbox(self.window, from_=0, textvariable=self.count_var, to=math.inf)
        self.count_dial.grid(column=0, row=2, columnspan=2)

        self.time_label = Label(self.window, text="Ring after time(in minutes) reaches: ")
        self.time_label.grid(column=0, row=3, columnspan=2)

        self.time_var = IntVar(self.window, value=0)
        self.time_dial = Spinbox(self.window, from_=0, textvariable=self.time_var, to=math.inf)
        self.time_dial.grid(column=0, row=4, columnspan=2)

        self.mode_label = Label(self.window, text="Mode: ")
        self.mode_label.grid(column=0, row=5, columnspan=1)
        self.mode_var = StringVar(self.window, value="OR")
        self.combo_box = Combobox(self.window, values=["OR", "AND"], textvariable=self.mode_var)
        self.combo_box.grid(column=1, row=5, columnspan=1)

        self.sound_label = Label(self.window, text="Select Alarm: ")
        self.sound_label.grid(column=0, row=6, columnspan=1)
        self.sound_file = StringVar(self.window, value=AlarmCreator.sound_files[0])
        self.combo_box = Combobox(self.window, values=AlarmCreator.sound_files, textvariable=self.sound_file)
        self.combo_box.grid(column=1, row=6, columnspan=1)

        def add_and_close():
            app.add_alarm(Alarm(path.join(AlarmCreator.sounds_folder, self.sound_file.get()), parent, self.mode_var.get(), self.count_var.get(), self.time_var.get() * 60))
            self.window.destroy()

        self.btn = ttk.Button(self.window, text="Add", command=add_and_close)
        self.btn.grid(column=0, row=7, columnspan=2)

    @staticmethod
    def load_sounds():
        sounds = os.listdir(AlarmCreator.sounds_folder)
        AlarmCreator.sound_files = sounds
