from Application import Application
from pynput.keyboard import Key, Listener

from AlarmCreator import AlarmCreator


class Program:
    def __init__(self):
        self.app = Application()
        self.control = False
        self.valid_keys = {"'+'", "'='", "<187>", "<107>"}
        self.valid_modifiers = {Key.alt_l, Key.alt_r, Key.alt, Key.alt_gr}

        def on_press(key):
            if key in self.valid_modifiers:
                self.control = True

        def on_release(key):
            if key in self.valid_modifiers:
                self.control = False
            if self.control and str(key) in self.valid_keys:
                print(key)
                self.app.add()

        keyboard = Listener(on_press, on_release)
        keyboard.start()

        AlarmCreator.load_sounds()
        self.app.run()


Program()
