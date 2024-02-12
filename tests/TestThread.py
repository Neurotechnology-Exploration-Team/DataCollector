import os.path
import random
import threading
from time import sleep

from pygame import mixer

import config
from LSL import LSL
from tests.TestGUI import TestGUI


class TestThread(threading.Thread):
    """
    A class that all tests should extend that holds all threading logic, initialization, and data logging.
    """

    def __init__(self, name):
        """
        The constructor that sets up the test name and stop condition.
        """
        super().__init__()

        # Setup name and trial number
        self.name = name
        self.trial_number = TestGUI.tests[self.name]["trial"]

        # Setup save path and create directories
        test_path = os.path.join(config.DATA_PATH, TestGUI.participant_ID, TestGUI.session_ID, self.name)
        self.current_path = os.path.join(str(test_path), f"trial_{str(self.trial_number).zfill(2)}")
        os.makedirs(self.current_path, exist_ok=True)

        self.iteration = 0
        self.current_label = None

        mixer.init()
        self.sound = mixer.Sound(os.path.join(os.path.dirname(__file__), '..', 'assets', 'beep.mp3'))

        self.running = True
        self._stop_event = threading.Event()  # Setup stop event to auto kill thread

    def run(self):
        """
        All logic related to the control panel, starting collection, and calling the stop method after a certain duration.
        """
        TestGUI.start_test(self.name)

        print(f"Starting test {self.name}: Trial {self.trial_number}")

        LSL.start_collection()  # Start LSL collection

        sleep(config.DATA_PADDING_DURATION)  # This gives the data collection a five second padding of rest

        def loop():
            """
            Main loop that runs and schedules the next iteration of the test
            """
            if self.iteration == config.ITERATIONS_PER_ACTION:
                self.running = False

            if self.running:
                # Setup next interval
                interval = random.randint(config.TEST_MIN_INTERVAL, config.TEST_MAX_INTERVAL)
                TestGUI.display_window.after(interval, loop)

                self.start_iteration()
            else:
                # Stop test thread
                TestGUI.display_window.after(1, self.stop)

            self.iteration += 1

        loop()

        return  # End thread

    def start_iteration(self):
        """
        Override this method with super().start_iteration() to create behavior at the beginning of each test iteration.
        """
        TestGUI.display_window.after(config.ITERATION_DURATION, self.stop_iteration)

    def stop_iteration(self):
        """
        Override this method with super().stop_iteration() to create behavior at the end of each test iteration.
        """
        pass

    def stop(self):
        """
        All logic relating to shutting down the test thread and stopping data collection.
        """
        LSL.stop_label()  # Stop labelling
        sleep(config.DATA_PADDING_DURATION)  # Wait to collect junk data

        LSL.stop_collection(self.current_path)  # Stop collecting

        complete = TestGUI.confirm_current_test(self.current_path)
        # Log finalized test status
        print(
            f"{TestGUI.current_test} - Trial {TestGUI.tests[TestGUI.current_test]['trial']}: {'Complete' if complete else 'Discarded'}")

        if not complete:  # If test is not complete
            TestGUI.tests[self.name]["trial"] += 1  # Increase trial number OUTSIDE OF THREAD!!!

        self._stop_event.set()  # Set the stop event so Python auto-kills the thread

    def stopped(self):
        """
        Overrides default stop method, as soon as stop event is set in stop() the test will auto kill itself.
        """
        return self._stop_event.is_set()

    def playsound(self):
        self.sound.play()
