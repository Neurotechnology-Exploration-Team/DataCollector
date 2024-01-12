import tkinter as tk
import importlib
import os
import threading

from TestGUI import TestGUI
import config
from LSL import LSL


class DataCollectorApp:
    """
    Class as a collection of all functions that interact with the test GUI
    """
    def __init__(self, lsl, test_gui):
        self.lsl = lsl
        self.test_gui = test_gui

    def run_test(self, test_name):
        """
        Connect to lsl and run the test in a thread

        :param test_name: Name of test being run
        """
        test_class = getattr(importlib.import_module(f"tests.{test_name}"), test_name)
        test = test_class(self.test_gui, self.lsl)

        test.start()  # Start test thread
        # TODO does this data overwrite? What happens if multiple tests are ran and a few are rejected?

    def run(self):
        """
        Main function for collecting data using the tkinter application
        """
        os.makedirs(config.DATA_PATH, exist_ok=True)

        test_directory = 'tests'
        test_names = [filename.split('.')[0]
                      for filename in os.listdir(test_directory)
                      if filename.endswith('.py') and not filename.startswith('Test')]

        for test_name in test_names:
            test_gui.add_button(test_name, lambda name=test_name: self.run_test(name))

        test_gui.control_window.mainloop()


if __name__ == '__main__':
    lsl = LSL()
    test_gui = TestGUI()
    app = DataCollectorApp(lsl, test_gui)
    app.run()
