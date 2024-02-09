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

        image_directory = os.path.join(os.path.dirname(__file__), '..', 'assets', 'Blink.png')
        self.image = tk.PhotoImage(file=image_directory)
        self.blink_label = None

    def start_iteration(self):
        super().start_iteration()

        self.blink_label = tk.Label(TestGUI.display_window, image=self.image, borderwidth=0)
        self.blink_label.place(relx=0.5, rely=0.5, anchor='center')

    def stop_iteration(self):
        super().stop_iteration()

        self.blink_label.destroy()
