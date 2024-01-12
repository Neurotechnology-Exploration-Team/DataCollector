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

    @staticmethod
    def run_test(test_name, lsl: LSL, test_gui):
        """
        Connect to lsl and run the test in a thread

        :param test_name: Name of test being run
        :param lsl: LSL connection to openBCI
        :param test_gui: Window from TKinter
        """
        test_class = getattr(importlib.import_module(f"tests.{test_name}"), test_name)
        test = test_class(test_gui, lsl)

        test.start()  # Start test thread
        # TODO does this data overwrite? What happens if multiple tests are ran and a few are rejected?

    @staticmethod
    def main():
        """
        Main function for collecting data using the tkinter application
        """
        os.makedirs(config.DATA_PATH, exist_ok=True)
        lsl = LSL()

        test_gui = TestGUI()

        test_directory = 'tests'
        test_names = [filename.split('.')[0]
                      for filename in os.listdir(test_directory)
                      if filename.endswith('.py') and not filename.startswith('Test')]

        def create_lambda(test_name):
            return lambda: DataCollectorApp.run_test(test_name, lsl, test_gui)

        for test_name in test_names:
            btn = tk.Button(test_gui.control_window, text=test_name)
            btn.config(command=create_lambda(test_name))
            btn.pack()
            test_gui.test_buttons[test_name] = btn

        test_gui.control_window.mainloop()


if __name__ == '__main__':
    DataCollectorApp.main()
