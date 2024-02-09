import tkinter as tk
from LSL import LSL
import os

from tests.TestGUI import TestGUI
from tests.TestThread import TestThread


class EyeOpenToEyeClosed(TestThread):
    """
    The Eyes Open to Eyes Closed test that extends the TestThread class.

    Explain to the subject they will be starting with their eyes closed.
    They will be switching between closed and open state when a cue is presented.
    The subject will know when to switch states by looking for two audiovisual cues denoting each action.
    TODO Due to the nature of the trial it will not be possible to have a visual stimulus for the eye closed to open transition.
    TODO Label for entire transition state?
    """

    def __init__(self):
        """
        Initializes and creates the transition labels in the display window.
        """
        super().__init__(transition=True)
        open_image_directory = os.path.join(os.path.dirname(__file__), '..', 'assets', 'EyesOpen.png')
        closed_image_directory = os.path.join(os.path.dirname(__file__), '..', 'assets', 'EyesClosed.PNG')

        self.open_image = tk.PhotoImage(file=open_image_directory)
        self.closed_image = tk.PhotoImage(file=closed_image_directory)

        self.firstImage = True
        self.current_label = None

    def start_iteration(self):
        """
        Creates and displays a new label for each iteration.
        """
        super().start_iteration()

        if self.firstImage:
            LSL.start_label("Open")
            self.current_label = tk.Label(TestGUI.display_window, image=self.open_image, borderwidth=0)
        else:
            LSL.start_label("Closed")
            self.current_label = tk.Label(TestGUI.display_window, image=self.closed_image, borderwidth=0)

        self.firstImage = not self.firstImage
        self.current_label.place(relx=0.5, rely=0.5, anchor='center')

    def stop_iteration(self):
        """
        Destroys the label after each iteration.
        """
        super().stop_iteration()

        self.current_label.destroy()

