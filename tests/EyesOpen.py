import tkinter as tk
import os

from tests.TestGUI import TestGUI
from tests.TestThread import TestThread


class EyesOpen(TestThread):
    """
    The Eyes Open test that extends the TestThread class.

    Explain to the subject they will be starting with their eyes open.
    Explain to the subject they will maintain a clear mind (try not to think about or focus on anything in particular) with eyes open.
    No auditory stimulus will be presented.
    """

    def __init__(self):
        """
        Initializes the image assets for the display window.
        """
        super().__init__()

        image_directory = os.path.join(os.path.dirname(__file__), '..', 'assets', 'EyesOpen.png')
        self.image = tk.PhotoImage(file=image_directory)
        self.eye_label = None

    def start_iteration(self):
        """
        Creates and displays a new label for each iteration.
        """
        super().start_iteration()

        self.eye_label = tk.Label(TestGUI.display_window, image=self.image, borderwidth=0)
        self.eye_label.place(relx=0.5, rely=0.5, anchor='center')

    def stop_iteration(self):
        """
        Destroys the label after each iteration.
        """
        super().stop_iteration()

        self.eye_label.destroy()
