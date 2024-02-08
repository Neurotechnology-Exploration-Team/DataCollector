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


class StationaryToLeft(TestThread):
    """
    The Blink test that extends the TestThread class. Each method should call its super() equivalent to ensure data collection and thread management.
    """

    def __init__(self):
        """
        Initializes and creates the blink label in the display window.
        """
        super().__init__()
        self.action_image_directory = os.path.join(os.path.dirname(__file__), '..', 'assets', 'Left.PNG')
        self.action_image = tk.PhotoImage(file=self.action_image_directory)
        self.stop_image_directory = os.path.join(os.path.dirname(__file__), '..', 'assets', 'stop white.PNG')
        self.stop_image = tk.PhotoImage(file=self.stop_image_directory)
        self.firstImage = True


    def run_iteration(self):
        super().run_iteration()
        current_Label = None
        if self.running:
            # Setup next interval
            interval = random.randint(config.TEST_MIN_INTERVAL, config.TEST_MAX_INTERVAL)
            TestGUI.display_window.after(interval, self.run_iteration)

        if self.firstImage:
            LSL.start_label("Stop")
            current_Label = tk.Label(TestGUI.display_window, image=self.stop_image, borderwidth=0)
        else:
            LSL.start_label("Left")
            current_Label =  tk.Label(TestGUI.display_window, image=self.action_image, borderwidth=0)
        
        self.firstImage = not self.firstImage
        def stop_iteration():   # Using this to destroy the blink label but also to start the labeler as Rest for default rest state
                    current_Label.destroy()
                    LSL.stop_label()
        current_Label.place(relx=0.5, rely=0.5, anchor='center')
        TestGUI.display_window.after(1000, stop_iteration)