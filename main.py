import importlib
import os

import config
from LSL import LSL
# from tests.TestGUI import TestGUI
# from tests.TestThread import TestThread


class DataCollectorApp:

    @staticmethod
    def run():
        """
        Main function for adding buttons that run tests to the GUI and initializing the LSL streams & GUI.
        """
        # Initialize streams & GUI
        LSL.init_lsl_stream()
        # TestGUI.init_gui()

        # Add each test button to the GUI that calls the run_test method above w/ the test name and type
        # for test_type in config.TESTS.keys():
        #     for test_name in config.TESTS[test_type]:
        #         # Add button to test
        #         TestGUI.add_test(test_name,
        #                          lambda n=test_name, t=test_type: DataCollectorApp.run_test(n, t))

        # TestGUI.control_window.mainloop()


if __name__ == '__main__':
    DataCollectorApp.run()
