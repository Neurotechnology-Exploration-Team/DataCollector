"""
THIS IS AN EXAMPLE OF WHAT A TEST CLASS SHOULD LOOK LIKE. DUPLICATE THIS CLASS AND UPDATE LABELS, ETC TO CREATE A NEW TEST.
"""
import random
import tkinter as tk

from tests.TestGUI import TestGUI
from tests.TestThread import TestThread


class EyesClose(TestThread):
    """
    The Blink test that extends the TestThread class. Each method should call its super() equivalent to ensure data collection and thread management.
    """

    def __init__(self):
        """
        Initializes and creates the blink label in the display window.
        """
        super().__init__()

        self.eye_label = tk.Label(TestGUI.display_window, text="Eyes Closed", font=("Helvetica", 16))
        self.eye_label.pack()



    def run(self):
        """
        Holds the logic to toggle blinking. TestThread will automatically call stop after the duration has ended.
        """
        super().run()


    def stop(self):
        """
        Toggles blinking flag and destroys label.
        """
        self.eye_label.destroy()

        super().stop()
