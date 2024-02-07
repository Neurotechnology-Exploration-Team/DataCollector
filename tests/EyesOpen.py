"""
THIS IS AN EXAMPLE OF WHAT A TEST CLASS SHOULD LOOK LIKE. DUPLICATE THIS CLASS AND UPDATE LABELS, ETC TO CREATE A NEW TEST.
"""
import random
import tkinter as tk

import os

import config

from tests.TestGUI import TestGUI
from tests.TestThread import TestThread


class EyesOpen(TestThread):
    """
    The Blink test that extends the TestThread class. Each method should call its super() equivalent to ensure data collection and thread management.
    """

    def __init__(self):
        """
        Initializes and creates the blink label in the display window.
        """
        super().__init__()

        self.image_directory = os.path.join(os.path.dirname(__file__), '..', 'assets', 'EyesClosed.png')
        self.image = tk.PhotoImage(file=self.image_directory)
        self.eye_label = tk.Label(TestGUI.display_window, image=self.image, borderwidth=0)

        self.keep_going = True
        self.eyes = True

        self.interval_time = random.randint(config.TEST_LOW_INTERVALS, config.TEST_HIGH_INTERVALS)

        self.trail = 0


    def run(self):
        """
        Holds the logic to toggle blinking. TestThread will automatically call stop after the duration has ended.
        """
        super().run()

        def toggle():
            if self.trail == config.TRAILS_PER_ACTION:
                TestGUI.display_window.after(1, self.stop)

            if self.eyes and self.keep_going:
                TestGUI.display_window.bell()
                self.brow_label.place(relx = 0.5, rely = 0.5, anchor='center')
                self.brow = False
                TestGUI.display_window.after(self.interval_time, toggle)
                self.trail += 1
            else:
                self.eye_label.place_forget()
                self.eyes = True
                TestGUI.display_window.after(1000, toggle)

            print (self.trail)

        toggle()



    def stop(self):
        """
        Toggles blinking flag and destroys label.
        """
        self.eye_label.destroy()
        self.keep_going = False
        self.eyes = False
        self.trail = 0
        super().stop()
