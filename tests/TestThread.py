import os.path
import threading
from time import sleep

from LSL import LSL

import config
from tests.TestGUI import TestGUI


class TestThread(threading.Thread):
    """
    A class that all tests should extend that holds all threading logic, initialization, and data logging.
    """

    def __init__(self):
        """
        The constructor that sets up the test name and stop condition.
        """
        super().__init__()

        self.name = self.__class__.__name__  # Test name is class name
        self.test_path = os.path.join(config.DATA_PATH, TestGUI.subject_number, self.name)
        self.trial = 0

        self._stop_event = threading.Event()  # Setup stop event to auto kill thread

    def run(self):
        """
        All logic related to the control panel, starting collection, and calling the stop method after a certain duration.
        """
        TestGUI.disable_buttons(self.name)

        LSL.start_collection()  # Start LSL collection

        sleep(config.DATA_PADDING_DURATION)  # TODO verify that this works since things are on separate threads

        LSL.start_label(self.name)


        # The type of test determines how long the test should run for
        if "To" in self.name:
            TestGUI.display_window.after(config.TRANSITION_TEST_DURATION, self.stop)
        else:
            TestGUI.display_window.after(config.TEST_DURATION, self.stop)


        return  # End thread

    def stop(self):
        """
        All logic relating to shutting down the test thread and stopping data collection.
        """
        LSL.stop_label()  # Stop labelling
        sleep(config.DATA_PADDING_DURATION)  # Wait to collect junk data

        current_path = os.path.join(str(self.test_path), f"trial_{str(self.trial).zfill(2)}")
        os.makedirs(current_path, exist_ok=True)

        LSL.stop_collection(current_path)  # Stop collecting

        if not TestGUI.confirm_current_test(current_path):
            self.trial += 1
            self.run()
        else:
            self._stop_event.set()  # Set the stop event so Python auto-kills the thread

    def stopped(self):
        """
        Overrides default stop method, as soon as stop event is set in stop() the test will auto kill itself.
        """
        return self._stop_event.is_set()
