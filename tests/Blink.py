import random
import tkinter as tk

from tests.TestGUI import TestGUI
from tests.TestThread import TestThread


class Blink(TestThread):
    def __init__(self):
        super().__init__(5000)

        self.blink_label = tk.Label(TestGUI.display_window, text="Blinking Text", font=("Helvetica", 16))
        self.blink_label.pack()

        self.blinking = True

    def stop(self):
        self.blinking = False
        self.blink_label.destroy()

        super().stop()

    def run(self):
        super().run()

        def toggle_blink():
            if self.blinking:
                self.blink_label.config(fg="black" if self.blink_label.cget("fg") == "white" else "white")
                TestGUI.display_window.after(random.randint(1000, 3000), toggle_blink)  # Schedule the next toggle

        # Start the blinking effect
        toggle_blink()
