import importlib
import json
import os
import config

from tests.gui import TestGUI
from timer import Timer


class Controller:
    def __init__(self):
        # Setup test states: A dictionary with test name keys corresponding to sub-dictionaries with lambda, button,
        # trial_number, and completed parameters
        self.tests = {}
        self.current_thread = None
        self.gui_delay_id = None

        def abort_current_test():
            self.current_thread.stop()

        self.gui = TestGUI(self.exit, abort_current_test)

        self.timer = Timer(self.gui.timer_label)

        participantID, sessionID = self.gui.prompt_participant_info()
        print(f"Participant: {participantID}, Session: {sessionID}")
        self.participantID = participantID
        self.sessionID = sessionID

        self._read_save_state()

    def run_test(self, test_name: str, test_type: str):
        """
        Runs the specified test in a separate thread and collects data.
        :param test_name: Name of the test being run
        :param test_type: Type of the test being run: Blink, Constant, or Transition
        """
        module_name = test_type
        class_name = test_type.capitalize() + "Test"
        # Dynamically import the test from tests package & construct it w/ no parameters
        test_class = getattr(importlib.import_module(f"tests.{module_name}"), class_name)

        trial = self.tests[test_name]['trial']

        # Setup save path and create directories
        test_path = os.path.join(config.SAVED_DATA_PATH, self.participantID, self.sessionID, test_name, f"trial_{str(trial).zfill(2)}")
        os.makedirs(test_path, exist_ok=True)

        if test_type == "transition":
            assets = config.TESTS[test_type][test_name]
            test = test_class(self, test_name, test_path, os.path.join('.', 'assets', assets[0]), os.path.join('.', 'assets', assets[1]))
        elif test_type == "constant":
            test = test_class(self, test_name, test_path)
        elif test_type == "blink":
            test = test_class(self, test_name, test_path)
        else:
            # Invalid test type
            raise ValueError(f"Unknown test type: {test_type}")

        self.current_thread = test
        print(f"Starting test {test_name}: Trial {trial}")

        self.timer.start_timer()
        self.gui.disable_buttons(self.current_thread.name)

        test.start()  # Start test thread

    def add_test(self, name, type):
        # Configure test state
        if not self.tests.get(name):
            self.tests[name] = {'trial': 0, 'completed': False}
            print("Added test: " + name)
        else:
            test = self.tests[name]
            print(f"Added test from saved state: {name} - Trial: {test['trial']}, Completed: {test['completed']}")

        self.gui.add_test(name, lambda n=name, t=type: self.run_test(n, t))  # Add test with function run_test above
        self.gui.update_buttons(self._get_completed_tests())

    def stop_test(self):
        # Remove all children of display canvas
        for child in self.gui.display_canvas.winfo_children():
            child.destroy()

        # Cancel currently running timer
        self.gui.display_window.after_cancel(self.gui_delay_id)
        self.gui_delay_id = None

        self.timer.stop_timer()
        self.timer.reset_timer()

        # Confirm data
        complete = self.gui.confirm_data()

        current_test = self.current_thread.name
        # Log finalized test status
        print(f"{current_test} - Trial {self.tests[current_test]['trial']}: "
              f"{'Complete' if complete else 'Discarded'}")

        if not complete:  # If test is not complete
            self.tests[current_test]["trial"] += 1  # Increase trial number OUTSIDE OF THREAD!!!

        self.gui.update_buttons(self._get_completed_tests())

        self.gui.destroy_current_element()

    def exit(self):
        self._write_save_state()
        self.gui.exit_gui()

        print("Exiting Data Collector")
        exit(0)

    def start_delay(self, interval, function):
        self.gui_delay_id = self.gui.display_window.after(int(interval), function)

    def place_image(self, image):
        self.gui.place_image(image)

    def place_text(self, text):
        self.gui.place_text(text)

    def clear_display(self):
        self.gui.destroy_current_element()

    def _read_save_state(self):
        state_save_path = os.path.join(config.SAVED_DATA_PATH, self.participantID, self.sessionID, "test_states.json")
        if os.path.isfile(state_save_path):
            print("Found saved test states.")
            try:
                # Read data from file:
                self.tests = json.load(open(state_save_path))
            except:
                print("Error reading saved test states.")

    def _write_save_state(self):
        # Create save path if it doesn't exist
        state_save_path = os.path.join(config.SAVED_DATA_PATH, self.participantID, self.sessionID)
        if not os.path.exists(state_save_path):
            os.makedirs(state_save_path)
        state_save_path = os.path.join(str(state_save_path), "test_states.json")

        # Serialize test data into file:
        json.dump(self.tests, open(state_save_path, 'w'))
        print("Test data serialized to test_states.json")

    def _get_completed_tests(self):
        completed_tests = []
        for test_name in self.tests:
            if self.tests[test_name]['completed']:
                completed_tests.append(test_name)

        return completed_tests
