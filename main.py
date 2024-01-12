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
    def run_test(test_name, btn, lsl: LSL, display_window):
        """
        Connect to lsl and run the test in a thread

        :param test_name: Name of test being run
        :param btn: The test being run (which button was pushed)
        :param lsl: LSL connection to openBCI
        :param display_window: Window from TKinter
        """
        current_test_button = btn

        for button in DataCollectorApp.test_buttons.values():
            button.config(state="disabled")

        test_class = getattr(importlib.import_module(f"tests.{test_name}"), test_name)
        test = test_class(display_window, lsl)

        current_test_thread = threading.Thread(target=test.run)

        current_test_thread.start()  # Start test
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

        def create_lambda(test_name, btn):
            return lambda: DataCollectorApp.run_test(test_name, btn, lsl, test_gui.display_window)

        DataCollectorApp.test_buttons = {}
        for test_name in test_names:
            btn = tk.Button(test_gui.control_window, text=test_name)
            btn.config(command=create_lambda(test_name, btn))
            btn.pack()
            DataCollectorApp.test_buttons[test_name] = btn

        test_gui.control_window.mainloop()


if __name__ == '__main__':
    DataCollectorApp.main()
