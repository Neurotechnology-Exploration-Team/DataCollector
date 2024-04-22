import random
from time import sleep

import config
from lsl import LSL
from tests.thread import TestThread


class BlinkTest(TestThread):
    """
    The Blink test that extends the TestThread class.

    Audio only
    """

    def __init__(self, controller, name, save_path):
        super().__init__(controller, name, save_path)

    def run_test(self):
        """
        Main loop that runs and schedules the next iteration of the test
        """
        if self.iteration == config.ITERATIONS_PER_TEST:
            self.running = False

        if self.running:
            # Blink & setup next interval
            LSL.start_label(self.name)
            self.playsound()
            self.iteration += 1

            interval = random.randint(int(config.BLINK_MIN_INTERVAL * 1000), int(config.BLINK_MAX_INTERVAL * 1000))
            sleep(config.PAUSE_AFTER_TEST)  # Wait extra after blinking
            LSL.stop_label()

            self.controller.start_delay(interval, self.run_test)
        else:
            # Stop test thread
            self.running = False

            LSL.stop_label()
            self.stop()
