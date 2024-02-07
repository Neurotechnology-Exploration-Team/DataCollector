"""
THIS IS AN EXAMPLE OF WHAT A TEST CLASS SHOULD LOOK LIKE. DUPLICATE THIS CLASS AND UPDATE LABELS, ETC TO CREATE A NEW TEST.
"""
import random
import tkinter as tk

import os

from tests.TestGUI import TestGUI
from tests.TestThread import TestThread

import config

class Blink(TestThread):
    """
    The Blink test that extends the TestThread class. Each method should call its super() equivalent to ensure data collection and thread management.
    """

    def __init__(self):
        """
        Initializes and creates the blink label in the display window.
        """
        super().__init__()

        self.image_directory = os.path.join(os.path.dirname(__file__), '..', 'assets', 'Blink.png')
        self.image = tk.PhotoImage(file=self.image_directory)
        self.blink_label = tk.Label(TestGUI.display_window, image=self.image, borderwidth=0)

        # random thing to add to make sure this is working

        self.keep_going = True
        self.blinking = True

        self.interval_time = random.randint(config.TEST_LOW_INTERVALS, config.TEST_HIGH_INTERVALS)
        self.trial = 0

    def run(self):
        """
        Holds the logic to toggle blinking. TestThread will automatically call stop after the duration has ended.
        """
        super().run()

        def toggle_blink():

            if self.trial == config.TRIALS_PER_ACTION:
                TestGUI.display_window.after(1, self.stop)

            if self.blinking and self.keep_going:
                self.blink_label.place(relx = 0.5, rely = 0.5, anchor='center')
                # self.blink_label.config(fg="white" if self.blink_label.cget("fg") == "black" else "black")
                self.blinking = False
                TestGUI.display_window.after(random.randint(config.TEST_LOW_INTERVALS, config.TEST_HIGH_INTERVALS), toggle_blink)  # Schedule the next toggle
                self.trial += 1
            else:
                self.blink_label.place_forget()
                self.blinking = True
                TestGUI.display_window.after(1000, toggle_blink)

            print (self.trial)

        # Start the blinking effect
        toggle_blink()

    def stop(self):
        """
        Toggles blinking flag and destroys label.
        """
        self.blinking = False
        self.keep_going = False
        self.trial = 0
        super().stop()
