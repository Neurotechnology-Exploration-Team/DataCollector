"""
THIS IS AN EXAMPLE OF WHAT A TEST CLASS SHOULD LOOK LIKE. DUPLICATE THIS CLASS AND UPDATE LABELS, ETC TO CREATE A NEW TEST.
"""
import random
import tkinter as tk

from tests.TestGUI import TestGUI
from tests.TestThread import TestThread


class Action(TestThread):
    """
    The Blink test that extends the TestThread class. Each method should call its super() equivalent to ensure data collection and thread management.
    """

    def __init__(self, action_name, trial_number):
        """
        Initializes and creates the blink label in the display window.
        """
        self.label = action_name
        super().__init__(action_name, trial_number)

        self.action_label = tk.Label(TestGUI.display_window, text=self.label, font=("Helvetica", 16))
        self.action_label.pack()

        self.action = True
        self.name = action_name

    def run(self):
        """
        Holds the logic to toggle blinking. TestThread will automatically call stop after the duration has ended.
        """
        super().run()

        def toggle_action():
            if self.action:
                self.action_label.config(fg="black" if self.action_label.cget("fg") == "white" else "white")
                TestGUI.display_window.after(random.randint(1000, 3000), toggle_action)  # Schedule the next toggle

        # Start the blinking effect
        toggle_action()

    def stop(self):
        """
        Toggles blinking flag and destroys label.
        """
        self.action = False
        self.action_label.destroy()

        super().stop()
