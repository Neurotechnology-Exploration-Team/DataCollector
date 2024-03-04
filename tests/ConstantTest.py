import os
import tkinter as tk

import config
from lsl import start_label, stop_label
from test_gui import place_text, place_image, destroy_current_element
from tests.TestThread import TestThread


class ConstantTest(TestThread):
    """
    The Constant test that extends the TestThread class. Uses text to describe action and a stop sign to indicate
    breaks.

    Visual (text and stop image) only
    """

    def __init__(self, name):
        """
        Initializes the image asset for the display window.
        """
        super().__init__(name)

        self.pause_image = tk.PhotoImage(file=os.path.join('assets', 'stop red.PNG'))
        self.text = None

    def run_test(self):
        """
        Main loop that runs and schedules the next iteration of the test
        """
        if self.iteration == config.ITERATIONS_PER_CONSTANT_TEST:
            self.running = False

        if self.running:
            start_label(self.name)

            self.text = place_text(self.name)
            self.wait(destroy_current_element, 3000)

            def resume():
                """
                Resumes the test after a labeling buffer for the specified duration.
                """
                if self.running:
                    destroy_current_element()
                    self.wait(self.run_test, int(config.PAUSE_AFTER_TEST * 1000))

            def pause():
                """
                Stop labeling and show a stop sign to give the participant a break from the constant test.
                """
                stop_label()

                if self.running:
                    self.text = place_image(self.pause_image)
                    self.wait(resume, config.CONSTANT_TEST_BREAK * 1000)  # Resume

            self.wait(pause, config.CONSTANT_TEST_DURATION * 1000)  # Pause
            self.iteration += 1
        else:
            # Stop test thread
            self.running = False

            stop_label()
            self.stop()
