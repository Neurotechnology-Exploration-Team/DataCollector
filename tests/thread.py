import os.path
import threading
from time import sleep

from pygame import mixer

import config
from lsl import LSL


class TestThread(threading.Thread):
    """
    A class that all tests should extend that holds all threading logic, initialization, and data logging.
    """

    def __init__(self, controller, name):
        """
        The constructor that sets up the test name and stop condition.
        """
        super().__init__()
        self.controller = controller

        # Setup name and trial number
        self.name = name
        self.trial_number = self.controller.tests[self.name]["trial"]

        # Setup save path and create directories TODO move to controller
        test_path = os.path.join(config.SAVED_DATA_PATH, self.controller.participantID, self.controller.sessionID, self.name)
        self.current_path = os.path.join(str(test_path), f"trial_{str(self.trial_number).zfill(2)}")
        os.makedirs(self.current_path, exist_ok=True)

        # Setup test details: iteration, the running state, and the ID of the current timer
        self.iteration = 0
        self.running = True

        # Hold values here as well incase durations need to be modified
        self.transition_duration = config.TRANSITION_DURATION
        self.constant_duration = config.CONSTANT_TEST_DURATION

        # Setup beep using pygame
        mixer.init()
        self.sound = mixer.Sound(os.path.join(os.path.dirname(__file__), '..', 'assets', 'beep.mp3'))

        self._stop_event = threading.Event()  # Setup stop event to auto kill thread

    def run(self):
        """
        All logic related to the control panel, starting collection, and calling the stop method after a certain duration.
        """
        # If eyes test, cut transition duration in half
        if "eyes" in self.name.lower():
            config.TRANSITION_DURATION = int(config.TRANSITION_DURATION / 2)
            config.CONSTANT_TEST_DURATION = int(config.CONSTANT_TEST_DURATION / 2)

        self.controller.start_test(self)

        print(f"Starting test {self.name}: Trial {self.trial_number}")

        LSL.start_collection()  # Start LSL collection

        sleep(config.DATA_PADDING_DURATION)  # This gives the data collection a five second padding of rest

        LSL.start_label(self.name)

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
        LSL.stop_label()  # Stop labelling
        sleep(config.DATA_PADDING_DURATION)  # Wait to collect junk data

        LSL.stop_collection(self.current_path)  # Stop collecting

        self.controller.stop_test()

        # Restore durations if they were modified
        config.TRANSITION_DURATION = self.transition_duration
        config.CONSTANT_TEST_DURATION = self.constant_duration

        self._stop_event.set()  # Set the stop event so Python auto-kills the thread

    def abort(self):
        """
        Function to abort test and save current data to new trial
        """
        self.controller.stop_test()
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
