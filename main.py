import importlib
import os

import config
from LSL import LSL
from tests.TestGUI import TestGUI


class DataCollectorApp:
    """
    A collection of functions to initialize the GUI, tests, and setup test logic.
    """

    @staticmethod
    def run_test(test_name: str, test_type: str):
        """
        Runs the specified test in a separate thread and collects data.
        :param test_name: Name of the test being run

        TODO error handling
        """
        # Dynamically import the test from tests package & construct it w/ no parameters
        class_name = f"{test_type}Test"
        test_class = getattr(importlib.import_module(f"tests.{class_name}"), class_name)

        test = None

        if test_type == "Transition":
            assets = config.TESTS["transition"][test_name]
            test = test_class(test_name, os.path.join('.', 'assets', assets[0]), os.path.join('.', 'assets', assets[1]))
        elif test_type == "Constant":
            asset = config.TESTS["constant"][test_name]
            test = test_class(test_name, os.path.join('.', 'assets', asset))
        elif test_type == "Blink":
            test = test_class(test_name)
        else:
            # Invalid test type
            pass

        test.start()  # Start test thread

    @staticmethod
    def run():
        """
        Main function for adding buttons that run tests to the GUI and initializing the LSL streams & GUI.
        """
        # Initialize streams & GUI
        LSL.init_lsl_stream()
        TestGUI.init_gui()

        # Add each test button to the GUI that calls the run_test method above w/ the test name
        for test_type in config.TESTS.keys():
            for test_name in config.TESTS[test_type]:
                # Add button to test
                TestGUI.add_test(test_name, lambda name=test_name: DataCollectorApp.run_test(test_name, test_type))

        TestGUI.control_window.mainloop()


if __name__ == '__main__':
    DataCollectorApp.run()
