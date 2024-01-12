import random
import tkinter as tk

from tests.Test import Test


class Blink(Test):
    def __init__(self, display_window, lsl):
        super().__init__(5000, display_window, lsl)

        self.blink_label = tk.Label(self.display_window, text="Blinking Text", font=("Helvetica", 16))
        self.blink_label.pack()

        self.blinking = True

    def destroy(self):
        super().destroy()

        self.blinking = False
        self.blink_label.destroy()

    def run(self):
        super().run()

        def toggle_blink():
            if self.blinking:
                self.blink_label.config(fg="black" if self.blink_label.cget("fg") == "white" else "white")
                self.display_window.after(random.randint(1000, 3000), toggle_blink)  # Schedule the next toggle

        # Start the blinking effect
        toggle_blink()
