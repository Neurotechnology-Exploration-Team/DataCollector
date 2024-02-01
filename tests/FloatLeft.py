"""
THIS IS AN EXAMPLE OF WHAT A TEST CLASS SHOULD LOOK LIKE. DUPLICATE THIS CLASS AND UPDATE LABELS, ETC TO CREATE A NEW TEST.
"""
import random
import tkinter as tk
import os

from tests.TestGUI import TestGUI
from tests.TestThread import TestThread


class FloatLeft(TestThread):
    """
    The Blink test that extends the TestThread class. Each method should call its super() equivalent to ensure data collection and thread management.
    """

    def __init__(self):
        """
        Initializes and creates the blink label in the display window.
        """
        super().__init__()
        self.image_directory = os.path.join(os.path.dirname(__file__), '..', 'assets', 'left.PNG')
        self.image = tk.PhotoImage(file=self.image_directory)
        self.image_label = tk.Label(TestGUI.display_window, image=self.image, borderwidth=0)
        self.image_label.place(relx = 0.5, rely = 0.5, anchor='center')






    def run(self):
        """
        Holds the logic to toggle blinking. TestThread will automatically call stop after the duration has ended.
        """
        super().run()


    def stop(self):
        """
        Toggles blinking flag and destroys label.
        """
        self.image_label.destroy()
        super().stop()
