import os
import tkinter as tk

from tests.TestGUI import TestGUI
from tests.TestThread import TestThread


class StationaryFloat(TestThread):
    """
    The Stationary Float test that extends the TestThread class.
    """

    def __init__(self):
        """
        Initializes the image assets for the display window.
        """
        super().__init__()

        image_directory = os.path.join(os.path.dirname(__file__), '..', 'assets', 'stop white.png')
        self.image = tk.PhotoImage(file=image_directory)
        self.select_label = None

    def start_iteration(self):
        """
        Creates and displays a new label for each iteration.
        """
        super().start_iteration()

        self.select_label = tk.Label(TestGUI.display_window, image=self.image, borderwidth=0)
        self.select_label.place(relx=0.5, rely=0.5, anchor='center')

    def stop_iteration(self):
        """
        Destroys the label after each iteration.
        """
        super().stop_iteration()

        self.select_label.destroy()
