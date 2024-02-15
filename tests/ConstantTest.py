import os
import random
import tkinter as tk
from time import sleep

import config
from LSL import LSL
from tests.TestGUI import TestGUI
from tests.TestThread import TestThread


class ConstantTest(TestThread):
    """
    No auditory stimulus will be presented.
    """

    def __init__(self, name):
        """
        Initializes the image assets for the display window.
        """
        super().__init__(name)

        self.pause_image = tk.PhotoImage(file=os.path.join('assets', 'stop red.PNG'))
        self.text = None

    def run_test(self):
        """
        Main loop that runs and schedules the next iteration of the test
        """
        if self.iteration == config.ITERATIONS_PER_ACTION:
            self.running = False

        if self.running:
            LSL.start_label(self.name)

            self.text = TestGUI.place_text(self.name)
            self.test_job_id = TestGUI.display_window.after(3000, TestGUI.destroy_current_element)

            def resume():
                if self.running:
                    TestGUI.destroy_current_element()
                    self.test_job_id = TestGUI.display_window.after(1000, self.run_test)  # TODO config

            def pause():
                LSL.stop_label()
                if self.running:
                    self.text = TestGUI.place_image(self.pause_image)
                    self.test_job_id = TestGUI.display_window.after(5000, resume)  # Resume after 5 seconds TODO config, default 5

            self.test_job_id = TestGUI.display_window.after(20000, pause)  # Pause after 20 seconds TODO config, default 20
            self.iteration += 1
        else:
            # Stop test thread
            self.running = False

            LSL.stop_label()
            self.stop()
