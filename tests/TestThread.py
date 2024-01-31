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

    def __init__(self, action_name):
        """
        The constructor that sets up the test name and stop condition.

        :param action_name: The name of the action.
        """
        super().__init__()

        self.name = action_name
        self.trial_number = TestGUI.tests[self.name]["trial"]

        test_path = os.path.join(config.DATA_PATH, TestGUI.participant_ID, TestGUI.session_ID, self.name)
        self.current_path = os.path.join(str(test_path), f"trial_{str(self.trial_number).zfill(2)}")
        os.makedirs(self.current_path, exist_ok=True)

        self._stop_event = threading.Event()  # Setup stop event to auto kill thread

    def run(self):
        """
        All logic related to the control panel, starting collection, and calling the stop method after a certain duration.
        """
        TestGUI.disable_buttons(self.name)

        print(f"Starting test {self.name}: Trial {self.trial_number}")

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
        # Log finalized test status
        print(f"{TestGUI.current_test} - Trial {TestGUI.tests[TestGUI.current_test]['trial']}: {'Complete' if complete else 'Discarded'}")

        # EXIT LOGIC TODO Add button
        if TestThread.__all_tests_complete():
            TestGUI.control_window.quit()
            print("All tests complete.")

        if not complete:  # If test is not complete
            TestGUI.tests[self.name]["trial"] += 1  # Increase trial number OUTSIDE OF THREAD!!!

        self._stop_event.set()  # Set the stop event so Python auto-kills the thread

    def stopped(self):
        """
        Overrides default stop method, as soon as stop event is set in stop() the test will auto kill itself.
        """
        return self._stop_event.is_set()

    @staticmethod
    def __all_tests_complete() -> bool:
        """
        Helper function to check the current state of all tests in the GUI.

        :return: True if all tests are complete, false otherwise.
        """
        for test in TestGUI.tests.keys():
            if not TestGUI.tests[test]['completed']:
                return False
        return True
