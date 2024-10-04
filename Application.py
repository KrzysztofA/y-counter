import json
import math
import statistics
from datetime import datetime
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *
import re
from pynput.keyboard import Key, Listener

from Alarm import Alarm
from AlarmCreator import AlarmCreator


class Application:
    def __init__(self):
        self.app = Tk()
        self.timer = ""
        self.delta = 0
        self.deltas = []
        self.sum = 0
        self.start = 0
        self.alarms = []
        self.var = IntVar(self.app, 0, "count")
        self.timeval = StringVar(self.app, value="00:00:00", name="total time")

        Label(self.app, textvariable=self.var).grid(column=0, row=1)
        self.stop_img = PhotoImage(file="icons8-stop-30.png")
        self.pause_img = PhotoImage(file="icons8-pause-30.png")
        self.start_img = PhotoImage(file="icons8-start-30.png")
        self.plus_img = PhotoImage(file="icons8-plus-30.png")

        self.btn = Button(self.app, image=self.plus_img, command=self.add)
        self.btn.grid(column=1, row=1)

        self.menu_bar = Menu(self.app)
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.settings_menu = Menu(self.menu_bar, tearoff=0)
        self.bool_var = BooleanVar(self.app, value=True)

        self.settings_menu.add_checkbutton(label="Always on top", variable=self.bool_var, onvalue=True, offvalue=False, command=self.set_always_on_top)
        self.file_menu.add_command(label="Save", command=self.save)
        self.file_menu.add_command(label="Load", command=self.load)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.menu_bar.add_separator()
        self.menu_bar.add_cascade(label="Settings", menu=self.settings_menu)
        self.settings_menu.add_command(label="Add Alarm", command=lambda: AlarmCreator(self, self.app))
        Label(self.app, textvariable=self.timeval).grid(column=0, row=2, columnspan=2)
        self.app.config(menu=self.menu_bar)
        self.pause_btn = Button(self.app, image=self.pause_img, command=self.pause_resume)
        self.pause_btn.grid(column=0, row=3)

        Button(self.app, image=self.stop_img, command=self.stop).grid(column=1, row=3)
        self.app.minsize(80, 100)
        self.app.maxsize(250, 150)
        self.app.attributes('-topmost', True)
        self.app.update()

    def pause_resume(self):
        print(self.btn["state"])
        if self.btn["state"] == NORMAL:
            self.btn.config(state=DISABLED)
            self.pause_btn.config(image=self.start_img)
            self.sum += self.delta
            self.delta = 0
            self.app.after_cancel(self.timer)
        else:
            self.btn.config(state=NORMAL)
            self.pause_btn.config(image=self.pause_img)
            self.start = datetime.now()
            self.timer = self.app.after(1000, self.update_time)

    def save(self):
        name = filedialog.asksaveasfilename(defaultextension="count")
        if name:
            with open(name, "w+") as file:
                json.dump({'count': self.var.get(), 'sum': self.sum + self.delta, 'deltas': self.deltas,
                           'alarms': [i.save() for i in self.alarms if not i.finished]}, file)

    def load(self):
        name = filedialog.askopenfilename(defaultextension="count")
        if name:
            with open(name) as file:
                json_data = json.load(file)
                self.sum = json_data["sum"]
                self.var.set(json_data["count"])
                self.start = datetime.now()
                self.delta = (datetime.now() - self.start).total_seconds()
                delta = self.sum + self.delta
                self.deltas = json_data["deltas"]
                self.timeval.set(f"{int(delta / 3600):02d}:{int((delta / 60) % 60):02d}:{int(delta % 60):02d}")
                arr = list(json_data['alarms'])
                self.alarms = [Alarm.load(alarm, self.app) for alarm in arr]

    def add_alarm(self, alarm: Alarm):
        self.alarms.append(alarm)

    def add(self):
        self.var.set(self.var.get() + 1)
        self.deltas.append(self.delta + self.sum)
        for i in self.alarms:
            i.update(self.var.get(), self.sum + self.delta)

    def update_time(self):
        self.delta = (datetime.now() - self.start).total_seconds()
        delta = self.sum + self.delta
        self.timeval.set(f"{math.floor(delta/3600):02d}:{int(math.floor(delta/60) % 60):02d}:{int(delta % 60):02d}")
        self.timer = self.app.after(1000, self.update_time)
        for i in self.alarms:
            i.update(self.var.get(), self.sum + self.delta)

    def set_always_on_top(self):
        if self.bool_var.get():
            self.app.attributes('-topmost', True)
            self.app.update()
        else:
            self.app.attributes('-topmost', False)
            self.app.update()

    def stop(self):
        self.app.after_cancel(self.timer)
        if self.var.get() > 0:
            with open(f"{int(self.delta * 10000 + self.sum)}{re.sub(r"\W", "", f"{datetime.now()}")}.txt", "w+") as file:
                file.write(f"Count: {self.var.get()}\n")
                file.write(f"Time Taken: {self.delta + self.sum}\n\n")
                file.write(f"Times:\n{"\n".join([f"{i}" for i in self.deltas])}\n\n")
                file.write("Stats:\n")
                file.write(f"Mean: {(self.delta + self.sum)/self.var.get()}\n")
                per_item_deltas = [self.deltas[0] if len(self.deltas) > 0 else 0]
                for i in range(1, len(self.deltas)):
                    per_item_deltas.append(self.deltas[i] - self.deltas[i-1])
                file.write(f"\nDurations:\n{"\n".join(f"{i}" for i in per_item_deltas)}\n\n")
                file.write(f"Standard Deviation: {statistics.stdev(per_item_deltas) if len(per_item_deltas) > 1 else 0}\n")
                file.write(f"Mode: {statistics.mode(per_item_deltas)}\n")
                file.write(f"Mean: {statistics.mean(per_item_deltas)}\n")
                file.write(f"Median: {statistics.median(per_item_deltas)}\n")
        self.delta = 0
        self.sum = 0
        self.deltas = []
        self.var.set(0)
        self.timeval.set('00:00:00')
        print(self.btn["state"])
        if self.btn["state"] == NORMAL:
            self.pause_resume()

    def run(self):
        self.start = datetime.now()
        self.timer = self.app.after(1000, self.update_time)
        self.app.geometry('85x105')
        self.app.title('Counter')
        self.app.mainloop()
