import importlib
import os

from lsl import LSL
from test_gui import TestGUI
import config


class DataCollectorApp:
    """
    Class as a collection of all functions that interact with the test GUI
    """

    @staticmethod
    def run_test(test_name):
        """
        Connect to lsl and run the test in a thread

        :param test_name: Name of test being run
        :param lsl_stream:
        """
        test_class = getattr(importlib.import_module(f"tests.{test_name}"), test_name)
        test = test_class()

        test.start()  # Start test thread
        # TODO does this data overwrite? What happens if multiple tests are ran and a few are rejected?

    @staticmethod
    def run():
        """
        Main function for collecting data using the tkinter application
        """
        os.makedirs(config.DATA_PATH, exist_ok=True)

        test_directory = 'tests'
        test_names = [filename.split('.')[0]
                      for filename in os.listdir(test_directory)
                      if filename.endswith('.py') and not filename.startswith('Test')]

        for test_name in test_names:
            TestGUI.add_button(test_name, lambda name=test_name: DataCollectorApp.run_test(name))

        TestGUI.control_window.mainloop()


if __name__ == '__main__':
    TestGUI.init_gui()
    LSL.init_lsl_stream()
    DataCollectorApp.run()
