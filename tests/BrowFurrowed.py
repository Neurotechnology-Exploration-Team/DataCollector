import os
import tkinter as tk

from tests.TestGUI import TestGUI
from tests.TestThread import TestThread


class BrowFurrowed(TestThread):
    """
    The Brow Furrowed test that extends the TestThread class.

    Explain to the subject they will be starting with their eyes open and brow furrowed.
    Explain to the subject they will maintain a clear mind with eyes open and continue to furrow their brow.
    No auditory stimulus will be presented.
    """

    def __init__(self):
        """
        Initializes the image assets for the display window.
        """
        super().__init__()

        image_directory = os.path.join(os.path.dirname(__file__), '..', 'assets', 'BrowFurrow.png')
        self.image = tk.PhotoImage(file=image_directory)
        self.brow_label = None

    def start_iteration(self):
        """
        Creates and displays a new label for each iteration.
        """
        super().start_iteration()

        self.brow_label = tk.Label(TestGUI.display_window, image=self.image, borderwidth=0)
        self.brow_label.place(relx=0.5, rely=0.5, anchor='center')

    def stop_iteration(self):
        """
        Destroys the label after each iteration.
        """
        super().stop_iteration()

        self.brow_label.destroy()
