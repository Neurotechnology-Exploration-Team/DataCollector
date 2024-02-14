import os
import tkinter as tk

from LSL import LSL
from tests.TestGUI import TestGUI
from tests.TestThread import TestThread


class ConstantTest(TestThread):
    """
    No auditory stimulus will be presented.

    TODO Add 10sec break
    """

    def __init__(self, name):
        """
        Initializes the image assets for the display window.
        """
        super().__init__(name, 60000)

        self.pause_image = tk.PhotoImage(file=os.path.join('assets', 'stop red.PNG'))
        self.label = None

    def start_iteration(self):
        """
        Creates and displays a new label for each iteration.
        """
        super().start_iteration()

        self.label = tk.Label(TestGUI.display_window, text=self.name, borderwidth=0)
        self.label.place(relx=0.5, rely=0.5, anchor='center')

        LSL.start_label(self.name)
        TestGUI.display_window.after(1000, self.label.destroy)

        def pause():
            LSL.stop_label()
            self.label = tk.Label(TestGUI.display_window, image=self.pause_image, borderwidth=0)
            self.label.place(relx=0.5, rely=0.5, anchor='center')

        TestGUI.display_window.after(40000, pause)

    def stop_iteration(self):
        """
        Destroys the label after each iteration.
        """
        if self.label:
            self.label.destroy()
