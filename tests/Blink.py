import os
import tkinter as tk
from pygame import mixer
from LSL import LSL
from tests.TestGUI import TestGUI
from tests.TestThread import TestThread


class Blink(TestThread):
    """
    The Blink test that extends the TestThread class.

    Explain to the subject they will be starting with their eyes open.
    They will be fully blinking when a cue is presented (eye close and open).
    Their eyes should always be open unless told to blink by the program.
    If they mistakenly blink too much or fail to blink, repeat the trial.
    """

    def __init__(self):
        """
        Initializes the image assets for the display window.
        """
        super().__init__()
        mixer.init()
        self.sound = mixer.Sound(os.path.join(os.path.dirname(__file__), '..', 'assets', 'beep.mp3'))
        image_directory = os.path.join(os.path.dirname(__file__), '..', 'assets', 'Blink.png')
        self.image = tk.PhotoImage(file=image_directory)
        self.blink_label = None

    def start_iteration(self):
        """
        Creates and displays a new label for each iteration.
        """
        super().start_iteration()
        
        self.blink_label = tk.Label(TestGUI.display_window, image=self.image, borderwidth=0)
        self.sound.play()
        self.blink_label.place(relx=0.5, rely=0.5, anchor='center')

    def stop_iteration(self):
        """
        Destroys the label after each iteration.
        """
        super().stop_iteration()

        self.blink_label.destroy()
        LSL.stop_label()
