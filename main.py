import config
from lsl import LSL
from tests.gui import TestGUI

from controller import Controller


def main():
    """
    Main function for adding buttons that run tests to the GUI and initializing the LSL streams & GUI.
    """
    # Initialize streams & GUI
    LSL.init_lsl_stream()
    controller = Controller()

    # Add each test button to the GUI that calls the run_test method above w/ the test name and type
    for test_type in config.TESTS.keys():
        for test_name in config.TESTS[test_type]:
            # Add button to test
            controller.add_test(test_name, test_type)

    controller.gui.control_window.mainloop()


if __name__ == '__main__':
    main()
