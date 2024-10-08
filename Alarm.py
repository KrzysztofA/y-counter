import json

import pydub

from tkinter import *
from tkinter import ttk

import simpleaudio

default_sound = "neraton.mp3"


class Alarm:
    def __init__(self, sound_file="neraton.mp3", parent=None, mode="OR", counter=0, time=0):
        try:
            self.tune = pydub.AudioSegment.from_mp3(sound_file)
        except:
            self.tune = pydub.AudioSegment.from_mp3(default_sound)
        self.sound_file = sound_file
        self.playback: any = None
        self.parent = parent
        self.counter = counter
        self.mode = mode
        self.time = time
        self.count_reached = False
        self.time_reached = False
        self.finished = False

    def update(self, count, time):
        if self.finished:
            return
        if self.counter != 0 and count >= self.counter:
            self.count_reached = True
        if self.time != 0 and time >= self.time:
            self.time_reached = True
        if self.time != 0 and self.counter != 0:
            if self.mode == "OR":
                if self.count_reached or self.time_reached:
                    self.play()
            elif self.mode == "AND":
                if self.count_reached and self.time_reached:
                    self.play()
        elif self.count_reached or self.time_reached:
            self.play()

    def popup_close(self):
        if self.playback:
            self.playback.stop()

    def play(self):
        self.finished = True
        self.playback = simpleaudio.play_buffer(
            self.tune.raw_data,
            num_channels=self.tune.channels,
            bytes_per_sample=self.tune.sample_width,
            sample_rate=self.tune.frame_rate
        )
        popup = Toplevel(self.parent)
        popup.title = "Alarm"
        ttk.Label(popup, text=f"{f"Counter of {self.counter} " if self.counter != 0 else ""}{f"{self.mode} " if self.time != 0 and self.counter != 0 else ""}{f"Time of {self.time}" if self.time != 0 else ""} reached!").pack()

        def popup_destroy_close():
            popup.destroy()
            self.popup_close()

        ttk.Button(popup, text="Ok", command=popup_destroy_close).pack()
        popup.protocol("WM_DELETE_WINDOW", self.popup_close)

    def save(self):
        if not self.finished:
            return { 'count': self.counter, 'mode': self.mode, 'time': self.time, 'time_reached': self.time_reached, 'count_reached': self.count_reached, 'sound_file': self.sound_file }
        else:
            return None

    @staticmethod
    def load(jsonobj, parent=None):
        counter = jsonobj['count']
        mode = jsonobj['mode']
        time = jsonobj['time']
        time_reached = jsonobj['time_reached']
        count_reached = jsonobj['count_reached']
        sound_file = jsonobj['sound_file']
        temp = Alarm(sound_file, parent, mode, counter, time)
        temp.count_reached = count_reached
        temp.time_reached = time_reached
        return temp
