import tkinter as tk

import matplotlib.pyplot as plt


class TestGUI:
    """
    Holds all logic relating to creating the GUI, adding buttons/windows, and the test confirmation window.
    """

    control_window = None
    display_window = None
    close_button = None
    abort_button = None

    # Setup test states: A dictionary with test name keys corresponding to sub-dictionaries with lambda, button,
    # trial_number, and completed parameters
    tests = {}
    current_thread = None

    participant_ID = ""
    session_ID = ""

    @staticmethod
    def init_gui():
        """
        MUST BE CALLED BEFORE ACCESSING ANY CLASS VARIABLES. Sets up the display window.
        """
        # Control window
        TestGUI.control_window = tk.Tk()
        TestGUI.control_window.title("Control Panel")
        TestGUI.__set_window_geometry(TestGUI.control_window, left_side=True)
        TestGUI.disable_close_button(TestGUI.control_window)

        # Test display window (child of control)
        TestGUI.display_window = tk.Toplevel(TestGUI.control_window)
        TestGUI.display_window.title("Display")
        TestGUI.display_window.configure(background='black')
        TestGUI.__set_window_geometry(TestGUI.display_window, left_side=False)
        TestGUI.disable_close_button(TestGUI.display_window)

        # Test lifecycle buttons (child of control)
        frame = tk.Frame(TestGUI.control_window)
        frame.pack(side="bottom", pady=100)

        TestGUI.abort_button = tk.Button(frame, text="ABORT TEST", height=4, width=30, state="disabled",
                                         command=lambda: TestGUI.current_thread.abort())
        TestGUI.abort_button.pack(side="left")

        TestGUI.close_button = tk.Button(frame, text="EXIT TESTING", height=4, width=30,
                                         command=lambda: TestGUI.__exit())
        TestGUI.close_button.pack(side="right")

        TestGUI.__prompt_participant_info()

    @staticmethod
    def add_test(test_name: str, test_lambda):
        """
        Adds a button to the test window with its name and function to run.

        :param test_name: The name of the test that the button will be assigned to.
        :param test_lambda: The function that the test will be ran with (no arguments).
        """
        # Configure button
        btn = tk.Button(TestGUI.control_window, text=test_name)
        btn.config(command=test_lambda, bg='red')
        btn.pack()

        # Configure test state
        TestGUI.tests[test_name] = {'lambda': test_lambda, 'button': btn, 'trial': 0, 'completed': False}
        print("Added test: " + test_name)

    @staticmethod
    def confirm_current_test() -> bool:
        """
        Run the test and prompt the user to confirm or deny the data.
        """
        # Confirm data
        TestGUI.__show_data_and_confirm()

        TestGUI.close_button.config(state="normal")
        TestGUI.abort_button.config(state="disabled")
        # Reset the buttons
        for test in TestGUI.tests.keys():
            if not TestGUI.tests[test]['completed']:  # If test is not complete, re-enable button
                TestGUI.tests[test]['button'].config(state="normal")
                TestGUI.tests[test]['button'].config(bg="red")
            else:  # If test is complete, set to green
                TestGUI.tests[test]['button'].config(state="disabled")
                TestGUI.tests[test]['button'].config(bg="green")

        # Clear graphs from memory
        plt.close()

        # Return true if test is complete
        return TestGUI.tests[TestGUI.current_thread.name]['completed']

    @staticmethod
    def start_test(test_thread):
        """
        A function to disable buttons while a test is running.

        :param test_thread: The thread object of the current test running (to enable the indicator).
        """
        # Disable all buttons
        TestGUI.close_button.config(state="disabled")
        TestGUI.abort_button.config(state="normal")

        for test in TestGUI.tests.keys():
            TestGUI.tests[test]['button'].config(state="disabled")

        # Indicate current test
        TestGUI.current_thread = test_thread
        TestGUI.tests[TestGUI.current_thread.name]['button'].config(bg="yellow")

    #
    # HELPER METHODS
    #

    @staticmethod
    def __show_data_and_confirm():
        """
        Popup the data confirmation window to check if it should be accepted or rejected,
        without displaying graphs.
        """
        popup = tk.Toplevel()
        popup.wm_title("Data Confirmation")
        TestGUI.disable_close_button(popup)
        popup.geometry("400x200")
        msg = tk.Label(popup, text="Confirm Test Data", font=("Arial", 12))
        msg.pack(pady=20)
        confirm_button = tk.Button(popup, text="Confirm", command=lambda: TestGUI.__handle_confirm(popup, True))
        deny_button = tk.Button(popup, text="Deny", command=lambda: TestGUI.__handle_confirm(popup, False))
        confirm_button.pack(side="left", padx=20, pady=20)
        deny_button.pack(side="right", padx=20, pady=20)
        popup.grab_set()
        TestGUI.control_window.wait_window(popup)

    @staticmethod
    def __handle_confirm(popup, confirmed):
        """
        Handle the confirmation or denial of data.
        """
        if confirmed:
            print("Data confirmed.")
        else:
            print("Data denied.")
        TestGUI.tests[TestGUI.current_thread.name]['completed'] = confirmed
        popup.destroy()
        for test_name, test_info in TestGUI.tests.items():
            if not test_info['completed']:
                test_info['button'].config(state="normal", bg="red")
            else:
                test_info['button'].config(state="disabled", bg="green")

    @staticmethod
    def __prompt_participant_info():
        """
        Creates a mandatory popup to prompt the user for the participant number and session,
        and sets TestGUI.participant_number and TestGUI.session to the result.
        Info that has to be collected: Participant:P001 Session:S001
        """

        popup = tk.Toplevel(TestGUI.control_window)
        TestGUI.disable_close_button(popup)
        popup.wm_title("Enter Participant Information")
        TestGUI.control_window.eval(f'tk::PlaceWindow {str(popup)} center')

        participant = tk.StringVar(value="P001")
        session = tk.StringVar(value="S001")

        def submit():
            TestGUI.participant_ID = participant.get()
            TestGUI.session_ID = session.get()
            print(f"Participant: {TestGUI.participant_ID}, Session: {TestGUI.session_ID}")

            popup.destroy()

        tk.Entry(popup, textvariable=participant).pack()
        tk.Entry(popup, textvariable=session).pack()

        submit_button = tk.Button(popup, text='Begin', command=submit)
        submit_button.pack()

        popup.grab_set()
        TestGUI.control_window.wait_window(popup)

    @staticmethod
    def __exit():
        """
        Helper function that handles the exit behavior of the GUI.
        """
        TestGUI.display_window.destroy()
        TestGUI.control_window.destroy()
        exit(0)

    @staticmethod
    def disable_close_button(window):
        """
        Helper function that disables the close/X button of the specified window.

        :param window: The window to disable the closing of.
        """
        def disable_event():
            pass

        window.protocol("WM_DELETE_WINDOW", disable_event)

    @staticmethod
    def __set_window_geometry(window, left_side=True):
        """
        Figure out size for a window and align it according to left_side

        :param window: Window passed from TKinter
        :param left_side: If it should be aligned on the left side or right
        """
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        width = screen_width // 2
        x = 0 if left_side else width
        window.geometry(f"{width}x{screen_height}+{x}+0")
