import os.path
import threading
from time import sleep

from pygame import mixer

import config
from lsl import start_collection, start_label, stop_label, stop_collection
from test_gui import display_window, tests, participant_ID, session_ID, start_test, confirm_current_test, current_thread, \
    destroy_current_element, display_canvas


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
        self.trial_number = tests[self.name]["trial"]

        # Setup save path and create directories
        test_path = os.path.join(config.SAVED_DATA_PATH, participant_ID, session_ID, self.name)
        self.current_path = os.path.join(str(test_path), f"trial_{str(self.trial_number).zfill(2)}")
        os.makedirs(self.current_path, exist_ok=True)

        # Setup test details: iteration, the running state, and the ID of the current timer
        self.iteration = 0
        self.running = True
        self.test_job_id = None

        # Setup beep using pygame
        mixer.init()
        self.sound = mixer.Sound(os.path.join(os.path.dirname(__file__), '..', 'assets', 'beep.mp3'))

        self._stop_event = threading.Event()  # Setup stop event to auto kill thread

    def run(self):
        """
        All logic related to the control panel, starting collection, and calling the stop method after a certain duration.
        """
        start_test(self)

        print(f"Starting test {self.name}: Trial {self.trial_number}")

        start_collection()  # Start LSL collection

        sleep(config.DATA_PADDING_DURATION)  # This gives the data collection a five second padding of rest

        start_label(self.name)

        self.run_test()

        return  # End thread

    def run_test(self):
        """
        Main loop that runs and schedules the next iteration of the test
        """
        pass  # Override me to implement a new test 💀

    def stop(self):
        """
        All logic relating to shutting down the test thread and stopping data collection.
        """
        stop_label()  # Stop labelling
        sleep(config.DATA_PADDING_DURATION)  # Wait to collect junk data

        stop_collection(self.current_path)  # Stop collecting

        complete = confirm_current_test()
        current_test = current_thread.name
        # Log finalized test status
        print(f"{current_test} - Trial {tests[current_test]['trial']}: "
              f"{'Complete' if complete else 'Discarded'}")

        if not complete:  # If test is not complete
            tests[self.name]["trial"] += 1  # Increase trial number OUTSIDE OF THREAD!!!

        destroy_current_element()

        self._stop_event.set()  # Set the stop event so Python auto-kills the thread

    def abort(self):
        """
        Function to abort test and save current data to new trial
        """
        # Remove all children of display canvas
        for child in display_canvas.winfo_children():
            child.destroy()

        # Cancel currently running timer
        display_window.after_cancel(self.test_job_id)
        self.test_job_id = None
        self.stop()

    def stopped(self):
        """
        Overrides default stop method, as soon as stop event is set in stop() the test will auto kill itself.
        """
        return self._stop_event.is_set()

    def playsound(self):
        """
        Helper method to play the constant sinusoidal beep sound for auditory stimulus (assets/beep.mp3).
        """
        self.sound.play()

    def wait(self, function, duration):
        """
        function to execute, duration in ms
        """
        self.test_job_id = display_window.after(duration, function)
