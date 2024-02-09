import os
import tkinter as tk

from tests.TestGUI import TestGUI
from tests.TestThread import TestThread


class FloatDown(TestThread):
    """
    The Float Down test that extends the TestThread class.

    Explain to the subject they will be imagining themselves floating downward in space.
    A visual stimulus will appear on the screen reminding the subject of the correct action.
    No auditory stimulus will be presented.

    TODO Label entire time?
    """

    def __init__(self):
        """
        Initializes the image assets for the display window.
        """
        super().__init__()

        image_directory = os.path.join(os.path.dirname(__file__), '..', 'assets', 'Down.png')
        self.image = tk.PhotoImage(file=image_directory)
        self.float_label = None

    def start_iteration(self):
        """
        Creates and displays a new label for each iteration.
        """
        super().start_iteration()

        self.float_label = tk.Label(TestGUI.display_window, image=self.image, borderwidth=0)
        self.float_label.place(relx=0.5, rely=0.5, anchor='center')

    def stop_iteration(self):
        """
        Destroys the label after each iteration.
        """
        super().stop_iteration()

        self.float_label.destroy()
