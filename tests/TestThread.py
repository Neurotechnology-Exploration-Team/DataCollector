"""
Uses "duck typing" to mock a template interface for what a test class should look like
"""
import threading

from lsl import EventLogger, LSL
from tests.TestGUI import TestGUI


class TestThread(threading.Thread):
    def __init__(self, duration):
        super().__init__()

        self.name = self.__class__.__name__
        self.duration = duration

        self._stop_event = threading.Event()

    def stop(self):
        """
        All logic related to destroying the test/any Tkinter widgets associated
        """
        EventLogger.record_timestamp(f"{self.name} End")
        LSL.stop_collection()

        TestGUI.confirm_test()

        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        """
        All logic related to the lifetime of the test
        """
        TestGUI.disable_buttons(self.name)

        LSL.start_collection()  # Start LSL collection
        EventLogger.record_timestamp(f"{self.name} Start")

        # Schedule to stop the test after 15 seconds
        TestGUI.display_window.after(self.duration, self.stop)

        return  # End thread
