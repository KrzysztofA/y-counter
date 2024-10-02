import json
import math
import statistics
from datetime import datetime
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *
import re

from Alarm import Alarm
from AlarmCreator import AlarmCreator


class Application:
    def __init__(self):

        app = Tk()
        self.timer: ""
        self.delta = 0
        self.deltas = []
        self.sum = 0
        self.start = datetime.now()
        self.alarms = []
        app.geometry('85x105')
        app.title('Counter')

        self.var = IntVar(app, 0, "count")
        timeval = StringVar(app, value="00:00:00", name="total time")

        Label(app, textvariable=self.var).grid(column=0, row=1)

        self.stop_img = PhotoImage(file="icons8-stop-30.png")
        self.pause_img = PhotoImage(file="icons8-pause-30.png")
        self.start_img = PhotoImage(file="icons8-start-30.png")
        self.plus_img = PhotoImage(file="icons8-plus-30.png")

        def add_counter():
            self.var.set(self.var.get() + 1)
            self.deltas.append(self.delta + self.sum)
            for i in self.alarms:
                i.update(self.var.get(), self.sum + self.delta)

        btn = Button(app, image=self.plus_img, command=add_counter)
        btn.grid(column=1, row=1)

        def update_time():
            self.delta = (datetime.now() - self.start).total_seconds()
            delta = self.sum + self.delta
            timeval.set(f"{math.floor(delta/3600):02d}:{int(math.floor(delta/60) % 60):02d}:{int(delta % 60):02d}")
            self.timer = app.after(1000, update_time)
            for i in self.alarms:
                i.update(self.var.get(), self.sum + self.delta)

        self.timer = app.after(1000, update_time)

        def pause_resume():
            print(btn["state"])
            if btn["state"] == NORMAL:
                btn.config(state=DISABLED)
                self.pause_btn.config(image=self.start_img)
                self.sum += self.delta
                self.delta = 0
                app.after_cancel(self.timer)
            else:
                btn.config(state=NORMAL)
                self.pause_btn.config(image=self.pause_img)
                self.start = datetime.now()
                self.timer = app.after(1000, update_time)

        def stop():
            app.after_cancel(self.timer)
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
            timeval.set('00:00:00')
            print(btn["state"])
            if btn["state"] == NORMAL:
                pause_resume()

        def save():
            name = filedialog.asksaveasfilename(defaultextension="count")
            if name:
                with open(name, "w+") as file:
                    json.dump({'count': self.var.get(), 'sum': self.sum + self.delta, 'deltas': self.deltas}, file)

        def load():
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
                    timeval.set(f"{int(delta / 3600):02d}:{int((delta / 60) % 60):02d}:{int(delta % 60):02d}")

        self.menu_bar = Menu(app)
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.settings_menu = Menu(self.menu_bar, tearoff=0)
        self.bool_var = BooleanVar(app, value=True)

        def set_always_on_top():
            if self.bool_var.get():
                app.attributes('-topmost', True)
                app.update()
            else:
                app.attributes('-topmost', False)
                app.update()

        self.settings_menu.add_checkbutton(label="Always on top", variable=self.bool_var, onvalue=True, offvalue=False, command=set_always_on_top)
        self.file_menu.add_command(label="Save", command=save)
        self.file_menu.add_command(label="Load", command=load)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.menu_bar.add_separator()
        self.menu_bar.add_cascade(label="Settings", menu=self.settings_menu)
        self.settings_menu.add_command(label="Add Alarm", command=lambda: AlarmCreator(self, app))
        Label(app, textvariable=timeval).grid(column=0, row=2, columnspan=2)
        app.config(menu=self.menu_bar)
        self.pause_btn = Button(app, image=self.pause_img, command=pause_resume)
        self.pause_btn.grid(column=0, row=3)

        Button(app, image=self.stop_img, command=stop).grid(column=1, row=3)
        app.minsize(80, 100)
        app.maxsize(250, 150)
        app.attributes('-topmost', True)
        app.update()

        app.mainloop()

    def add_alarm(self, alarm: Alarm):
        self.alarms.append(alarm)


Application()
