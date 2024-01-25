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

    def __init__(self, action_name, trial_number):
        """
        The constructor that sets up the test name and stop condition.

        :param action_name: The name of the action.
        :param trial_number: The trial number of the action.
        """
        super().__init__()

        self.name = action_name
        self.trial_number = trial_number

        test_path = os.path.join(config.DATA_PATH, TestGUI.subject_number, self.name)
        self.current_path = os.path.join(str(test_path), f"trial_{str(self.trial_number).zfill(2)}")
        os.makedirs(self.current_path, exist_ok=True)

        self.callback = None  # Callback for when a test is complete

        self._stop_event = threading.Event()  # Setup stop event to auto kill thread

    def run(self):
        """
        All logic related to the control panel, starting collection, and calling the stop method after a certain duration.
        """
        TestGUI.disable_buttons(self.name)

        LSL.start_collection()  # Start LSL collection

        sleep(config.DATA_PADDING_DURATION)  # TODO verify that this works since things are on separate threads

        LSL.start_label(self.name)

        # Schedule to stop the test after 15 seconds
        TestGUI.display_window.after(config.TEST_DURATION, self.stop)

        return  # End thread

    def stop(self):
        """
        All logic relating to shutting down the test thread and stopping data collection.
        """
        LSL.stop_label()  # Stop labelling
        sleep(config.DATA_PADDING_DURATION)  # Wait to collect junk data

        LSL.stop_collection(self.current_path)  # Stop collecting

        complete = TestGUI.confirm_current_test(self.current_path)

        if self.callback is not None:
            self.callback(complete)

        print("Test completed: " + self.name)
        self._stop_event.set()  # Set the stop event so Python auto-kills the thread

    def stopped(self):
        """
        Overrides default stop method, as soon as stop event is set in stop() the test will auto kill itself.
        """
        return self._stop_event.is_set()

    def set_callback(self, callback):
        """
        A function to set the callback for the test that takes in a boolean parameter completed.
        """
        self.callback = callback
