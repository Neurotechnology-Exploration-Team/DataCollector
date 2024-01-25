from LSL import LSL
from tests.TestGUI import TestGUI
from tests.Action import Action


class DataCollectorApp:
    """
    A collection of functions to initialize the GUI, tests, and setup test logic.
    """

    @staticmethod
    def run_test(test_name):
        """
        Runs the specified test in a separate thread and collects data.

        :param test_name: Name of the test being run
        """
        test = Action(test_name, TestGUI.tests[test_name]["trial"])
        test.start()

        def callback(test_complete):
            if DataCollectorApp.__all_tests_complete():
                TestGUI.control_window.quit()
                print("All tests complete.")

            if not test_complete:  # If test is not complete
                TestGUI.tests[test_name]["trial"] += 1  # Increase trial number OUTSIDE OF THREAD!!!

        test.set_callback(callback)

    @staticmethod
    def run():
        """
        Main function for adding buttons that run tests to the GUI and initializing the LSL streams & GUI.
        """
        # Initialize streams & GUI
        LSL.init_lsl_stream()
        TestGUI.init_gui()

        test_names = ['Blink', 'Brow Furrow', 'Brow Unfurrow', 'Stationary Floating', 'Float Left', 'Float Right',
                      'Float Up', 'Float Down', 'Select', 'Eyes Open', 'Eyes Closed']

        for test_name in test_names:
            # Add button to test
            TestGUI.add_button(test_name, lambda name=test_name: DataCollectorApp.run_test(name))

        TestGUI.control_window.mainloop()

    @staticmethod
    def __all_tests_complete() -> bool:
        """
        Helper function to check the current state of all tests in the GUI.

        :return: True if all tests are complete, false otherwise.
        """
        for test in TestGUI.tests.keys():
            if not TestGUI.tests[test]['completed']:
                return False
        return True


if __name__ == '__main__':
    DataCollectorApp.run()
