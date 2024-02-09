import tkinter as tk
from LSL import LSL
import os

from tests.TestGUI import TestGUI
from tests.TestThread import TestThread


class BrowFurrowToUnfurrow(TestThread):
    """
    The Brow Furrow to Unfurrowed test that extends the TestThread class.

    Explain to the subject they will be starting with their brow unfurrowed and eyes closed.
    They will be furrowing their brow when a cue is presented and then unfurrowing their brow when the next cue is presented.
    TODO The subject will know when to switch states by looking for two audiovisual cues denoting each action.
    TODO Label for entire transition state?
    """

    def __init__(self):
        """
        Initializes and creates the transition labels in the display window.
        """
        super().__init__(transition=True)
        furrow_image_directory = os.path.join(os.path.dirname(__file__), '..', 'assets', 'BrowFurrow.png')
        unfurrow_image_directory = os.path.join(os.path.dirname(__file__), '..', 'assets', 'BrowUnfurrow.PNG')

        self.furrow_image = tk.PhotoImage(file=furrow_image_directory)
        self.unfurrow_image = tk.PhotoImage(file=unfurrow_image_directory)

        self.firstImage = True
        self.current_label = None

    def start_iteration(self):
        """
        Creates and displays a new label for each iteration.
        """
        super().start_iteration()

        if self.firstImage:
            LSL.start_label("Brow Furrowed")
            self.current_label = tk.Label(TestGUI.display_window, image=self.furrow_image, borderwidth=0)
        else:
            LSL.start_label("Brow Unfurrowed")
            self.current_label = tk.Label(TestGUI.display_window, image=self.unfurrow_image, borderwidth=0)

        self.firstImage = not self.firstImage
        self.current_label.place(relx=0.5, rely=0.5, anchor='center')

    def stop_iteration(self):
        """
        Destroys the label after each iteration.
        """
        super().stop_iteration()

        self.current_label.destroy()

