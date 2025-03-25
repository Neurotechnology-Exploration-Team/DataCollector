import random
from time import sleep

import config
import tkinter as tk
from LSL import LSL
from tests.TestGUI import TestGUI
from tests.TestThread import TestThread


class BlinkTest(TestThread):
    """
    The Blink test that extends the TestThread class.
    """

    def __init__(self, name):
        super().__init__(name)
        self.blink_image = tk.PhotoImage(file="assets/Blink.png")
        self.empty_image = tk.PhotoImage(file="assets/Empty.png")
        self.current_image = None

    def run_test(self):
        """
        Main loop that runs and schedules the next iteration of the test
        """
        if self.iteration == config.ITERATIONS_PER_TEST:
            self.running = False

        if self.running:
            # Blink & setup next interval
            LSL.start_label(self.name)
            self.current_image = TestGUI.place_image(self.blink_image)
            TestGUI.display_window.update()
            self.playsound()
            self.iteration += 1

            interval = random.randint(int(config.BLINK_MIN_INTERVAL * 1000), int(config.BLINK_MAX_INTERVAL * 1000))
            sleep(config.PAUSE_AFTER_TEST)  # Wait extra after blinking

            TestGUI.destroy_current_element()
            self.current_image = TestGUI.place_image(self.empty_image)
            TestGUI.display_window.update()
            LSL.stop_label()

            self.test_job_id = TestGUI.display_window.after(interval, self.run_test)
        else:
            # Stop test thread
            self.running = False

            LSL.stop_label()
            self.stop()
