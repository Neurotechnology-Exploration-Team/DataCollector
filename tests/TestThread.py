import threading

from lsl import LSL
from tests.TestGUI import TestGUI


class TestThread(threading.Thread):
    """
    A class that all tests should extend that holds all threading logic, initialization, and data logging.
    """

    def __init__(self, duration):
        """
        The constructor that takes in a test duration.
        TODO this can probably be removed, put it in config instead
        """
        super().__init__()

        self.name = self.__class__.__name__  # Test name is class name
        self.duration = duration

        self._stop_event = threading.Event()  # Setup stop event to auto kill thread

    def stop(self):
        """
        All logic relating to shutting down the test thread and stopping data collection.
        """
        LSL.stop_collection()

        TestGUI.confirm_test()

        self._stop_event.set()

    def stopped(self):
        """
        Overrides default stop method, as soon as stop event is set in stop() the test will auto kill itself.
        """
        return self._stop_event.is_set()

    def run(self):
        """
        All logic related to the control panel, starting collection, and calling the stop method after a certain duration.
        """
        TestGUI.disable_buttons(self.name)

        LSL.start_collection(self.name)  # Start LSL collection

        # Schedule to stop the test after 15 seconds
        TestGUI.display_window.after(self.duration, self.stop)

        return  # End thread
