import tkinter as tk

from LSL import LSL
from tests.TestGUI import TestGUI
from tests.TestThread import TestThread


class ConstantTest(TestThread):
    """
    No auditory stimulus will be presented.

    TODO Add 10sec break
    """

    def __init__(self, name, image_directory):
        """
        Initializes the image assets for the display window.
        """
        super().__init__(name)

        self.image = tk.PhotoImage(file=image_directory)
        self.label = None

    def start_iteration(self):
        """
        Creates and displays a new label for each iteration.
        """
        super().start_iteration()

        self.label = tk.Label(TestGUI.display_window, image=self.image, borderwidth=0)
        self.label.place(relx=0.5, rely=0.5, anchor='center')

        LSL.start_label(self.name)

    def stop_iteration(self):
        """
        Destroys the label after each iteration.
        """

        self.label.destroy()
