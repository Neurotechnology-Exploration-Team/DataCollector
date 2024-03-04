import random
from time import sleep

import config
from lsl import start_label, stop_label
from tests.TestThread import TestThread


class BlinkTest(TestThread):
    """
    The Blink test that extends the TestThread class.

    Audio only
    """

    def __init__(self, name):
        super().__init__(name)

    def run_test(self):
        """
        Main loop that runs and schedules the next iteration of the test
        """
        if self.iteration == config.ITERATIONS_PER_TEST:
            self.running = False

        if self.running:
            # Blink & setup next interval
            start_label(self.name)
            self.playsound()
            self.iteration += 1

            interval = random.randint(config.BLINK_MIN_INTERVAL * 1000, config.BLINK_MAX_INTERVAL * 1000)
            sleep(config.PAUSE_AFTER_TEST)  # Wait extra after blinking
            stop_label()

            self.wait(self.run_test, interval)
        else:
            # Stop test thread
            self.running = False

            stop_label()
            self.stop()
