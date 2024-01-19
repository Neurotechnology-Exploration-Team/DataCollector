import importlib
import os

from LSL import LSL
from tests.TestGUI import TestGUI


class DataCollectorApp:
    """
    A collection of functions to setup the Tkinter GUI
    """

    @staticmethod
    def run_test(test_name):
        """
        Runs the specified test in a separate thread and collects data.

        :param test_name: Name of the test being run
        """
        # Dynamically import the test from tests package & construct it w/ no parameters
        test_class = getattr(importlib.import_module(f"tests.{test_name}"), test_name)
        test = test_class()

        test.start()  # Start test thread

    @staticmethod
    def run():
        """
        Main function for adding buttons that run tests to the GUI and initializing the LSL streams & GUI.
        """
        # Initialize streams & GUI
        LSL.init_lsl_stream()
        TestGUI.init_gui()

        # Locate all tests (filename should be the same as test name)
        test_directory = 'tests'
        test_names = [filename.split('.')[0]
                      for filename in os.listdir(test_directory)
                      if filename.endswith('.py') and not filename.startswith('Test')]

        for test_name in test_names:
            # Add button to test
            TestGUI.add_button(test_name, lambda name=test_name: DataCollectorApp.run_test(name))

        # TODO how do we know if all tests are complete? Close window when done.

        TestGUI.control_window.mainloop()


if __name__ == '__main__':
    DataCollectorApp.run()
