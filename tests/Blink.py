"""
THIS IS AN EXAMPLE OF WHAT A TEST CLASS SHOULD LOOK LIKE. DUPLICATE THIS CLASS AND UPDATE LABELS, ETC TO CREATE A NEW TEST.
"""
import random
import tkinter as tk
from LSL import LSL
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

    def run_iteration(self):
        super().run_iteration()

        if self.running:
            # Setup next interval
            interval = random.randint(config.TEST_MIN_INTERVAL, config.TEST_MAX_INTERVAL)
            TestGUI.display_window.after(interval, self.run_iteration)
            
        LSL.start_label("Blinking")
        blink_label = tk.Label(TestGUI.display_window, image=self.image, borderwidth=0)
        blink_label.place(relx=0.5, rely=0.5, anchor='center')

        def stop_iteration():   # Using this to destroy the blink label but also to start the labeler as Rest for default rest state
            blink_label.destroy()
            LSL.stop_label()
        TestGUI.display_window.after(1000, stop_iteration)


