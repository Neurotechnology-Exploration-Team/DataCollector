import os
import tkinter as tk

import config
from LSL import LSL
from tests.TestGUI import TestGUI
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
        if self.iteration == config.ITERATIONS_PER_ACTION:
            self.running = False

        if self.running:
            LSL.start_label(self.name)

            self.text = TestGUI.place_text(self.name)
            self.test_job_id = TestGUI.display_window.after(3000, TestGUI.destroy_current_element)

            def resume():
                """
                Resumes the test after a labeling buffer for the specified duration.
                """
                if self.running:
                    TestGUI.destroy_current_element()
                    self.test_job_id = TestGUI.display_window.after(int(config.PAUSE_AFTER_TEST * 1000), self.run_test)

            def pause():
                """
                Stop labeling and show a stop sign to give the participant a break from the constant test.
                """
                LSL.stop_label()

                if self.running:
                    self.text = TestGUI.place_image(self.pause_image)
                    self.test_job_id = TestGUI.display_window.after(config.CONSTANT_TEST_BREAK * 1000, resume)  # Resume

            self.test_job_id = TestGUI.display_window.after(config.CONSTANT_TEST_DURATION * 1000, pause)  # Pause
            self.iteration += 1
        else:
            # Stop test thread
            self.running = False

            LSL.stop_label()
            self.stop()
