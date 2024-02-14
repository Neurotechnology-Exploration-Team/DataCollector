import os
import random
from time import sleep

from pygame import mixer

import config
from LSL import LSL
from tests.TestGUI import TestGUI
from tests.TestThread import TestThread


class BlinkTest(TestThread):
    """
    The Blink test that extends the TestThread class.

    Audio only
    """

    def __init__(self, name):
        """
        Initializes the image assets for the display window.
        """
        super().__init__(name)  # TODO change to an arbitrary number, this should be 30 blinks

        self.blinking = False

    def run_test(self):
        """
        Main loop that runs and schedules the next iteration of the test
        """
        if self.iteration == config.ITERATIONS_PER_ACTION:
            self.running = False

        if self.running:
            # Blink & setup next interval
            LSL.start_label(self.name)
            self.playsound()
            self.iteration += 1

            interval = random.randint(config.BLINK_MIN_INTERVAL, config.BLINK_MAX_INTERVAL)
            sleep(0.5)  # Wait extra after blinking TODO config
            LSL.stop_label()

            TestGUI.display_window.after(interval, self.run_test)
        else:
            # Stop test thread
            self.blinking = False

            LSL.stop_label()
            self.stop()
            TestGUI.display_window.after(1, self.stop)
