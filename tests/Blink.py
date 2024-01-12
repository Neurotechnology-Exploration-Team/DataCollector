import random
import tkinter as tk

from tests.TestThread import TestThread


class Blink(TestThread):
    def __init__(self, test_gui, lsl):
        super().__init__(5000, test_gui, lsl)

        self.blink_label = tk.Label(self.test_gui.display_window, text="Blinking Text", font=("Helvetica", 16))
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
                self.test_gui.display_window.after(random.randint(1000, 3000), toggle_blink)  # Schedule the next toggle

        # Start the blinking effect
        toggle_blink()
