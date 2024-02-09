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


class StationaryToDown(TestThread):
    """
    The Blink test that extends the TestThread class. Each method should call its super() equivalent to ensure data collection and thread management.
    """

    def __init__(self):
        """
        Initializes and creates the blink label in the display window.
        """
        super().__init__(transition=True)
        action_image_directory = os.path.join(os.path.dirname(__file__), '..', 'assets', 'Down.PNG')
        self.action_image = tk.PhotoImage(file=action_image_directory)
        stop_image_directory = os.path.join(os.path.dirname(__file__), '..', 'assets', 'stop white.PNG')
        self.stop_image = tk.PhotoImage(file=stop_image_directory)
        self.firstImage = True

        self.current_label = None

    def start_iteration(self):
        super().start_iteration()

        if self.firstImage:
            LSL.start_label("Stop")
            self.current_label = tk.Label(TestGUI.display_window, image=self.stop_image, borderwidth=0)
        else:
            LSL.start_label("Down")
            self.current_label = tk.Label(TestGUI.display_window, image=self.action_image, borderwidth=0)

        self.firstImage = not self.firstImage
        self.current_label.place(relx=0.5, rely=0.5, anchor='center')

    def stop_iteration(self):
        super().stop_iteration()

        self.current_label.destroy()
