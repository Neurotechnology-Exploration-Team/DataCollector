import os
import tkinter as tk

from playsound import playsound

from LSL import LSL
from tests.TestGUI import TestGUI
from tests.TestThread import TestThread


class TransitionTest(TestThread):
    """
    TODO
    """

    def __init__(self, name, image_directory_1, image_directory_2):
        """
        Initializes and creates the transition labels in the display window.
        """
        super().__init__(name)

        self.image_1 = tk.PhotoImage(file=image_directory_1)
        self.image_2 = tk.PhotoImage(file=image_directory_2)

        # TODO fix labels
        self.label_1 = name.split("To")[0]
        self.label_2 = name.split("To")[1]

        self.firstImage = True
        self.current_label = None

    def start_iteration(self):
        """
        Creates and displays a new label for each iteration.
        """
        super().start_iteration()

        if self.firstImage:
            LSL.start_label(self.label_1)
            self.current_label = tk.Label(TestGUI.display_window, image=self.image_1, borderwidth=0)
        else:
            LSL.start_label(self.label_2)
            self.current_label = tk.Label(TestGUI.display_window, image=self.image_2, borderwidth=0)

        self.firstImage = not self.firstImage
        self.playsound()
        LSL.start_label(self.name)
        self.current_label.place(relx=0.5, rely=0.5, anchor='center')

    def stop_iteration(self):
        """
        Destroys the label after each iteration.
        """
        super().stop_iteration()

        self.current_label.destroy()

