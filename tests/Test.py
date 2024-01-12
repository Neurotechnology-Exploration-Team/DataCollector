"""
Uses "duck typing" to mock a template interface for what a test class should look like
"""
from LSL import EventLogger


class Test:
    def __init__(self, duration, display_window, lsl):
        self.duration = duration
        self.display_window = display_window
        self.lsl = lsl

        lsl.start_collection()  # Start LSL collection
        EventLogger.record_timestamp(f"{__class__} Start")

    def destroy(self):
        """
        All logic related to destroying the test/any Tkinter widgets associated
        """
        EventLogger.record_timestamp(f"{__class__} End")
        self.lsl.stop_collection()

    def run(self):
        """
        All logic related to the lifetime of the test
        """
        # Schedule to stop the test after 15 seconds
        self.display_window.after(self.duration, self.destroy)
