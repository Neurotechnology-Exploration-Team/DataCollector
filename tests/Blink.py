"""
THIS IS AN EXAMPLE OF WHAT A TEST CLASS SHOULD LOOK LIKE. DUPLICATE THIS CLASS AND UPDATE LABELS, ETC TO CREATE A NEW TEST.
"""
import random
import tkinter as tk

from tests.TestGUI import TestGUI
from tests.TestThread import TestThread


class Blink(TestThread):
    """
    The Blink test that extends the TestThread class. Each method should call its super() equivalent to ensure data collection and thread management.
    """

    def __init__(self, trial_number):
        """
        Initializes and creates the blink label in the display window.
        """
        super().__init__(trial_number)

        self.blink_label = tk.Label(TestGUI.display_window, text="Blinking Text", font=("Helvetica", 16))
        self.blink_label.pack()

        self.blinking = True

    def run(self):
        """
        Holds the logic to toggle blinking. TestThread will automatically call stop after the duration has ended.
        """
        super().run()

        def toggle_blink():
            if self.blinking:
                self.blink_label.config(fg="black" if self.blink_label.cget("fg") == "white" else "white")
                TestGUI.display_window.after(random.randint(1000, 3000), toggle_blink)  # Schedule the next toggle

        # Start the blinking effect
        toggle_blink()

    def stop(self):
        """
        Toggles blinking flag and destroys label.
        """
        self.blinking = False
        self.blink_label.destroy()

        super().stop()