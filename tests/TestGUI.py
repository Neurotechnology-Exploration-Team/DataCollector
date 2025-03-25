import os
import tkinter as tk
import threading
import time
import json
from queue import Queue

import config


class TestGUI:
    """
    Holds all logic relating to creating the GUI, adding buttons/windows, and the test confirmation window.

    This acts as an all-in-one test controller and GUI manager.
    """

    # Window variables
    control_window = None
    display_window = None
    display_canvas = None  # The canvas on the display window to display images/text
    close_button = None
    abort_button = None

    current_display_element = None  # The ID of the current element being displayed on display_canvas

    # Setup test states: A dictionary with test name keys corresponding to sub-dictionaries with lambda, button,
    # trial_number, and completed parameters
    tests = {}
    current_thread = None

    participant_ID = ""
    session_ID = ""

    # TODO possibly refactor timer into different class/module?
    timer_label = None
    timer_thread = None
    test_start_time = None
    timer_queue = None
    dynamic_test_duration = 0

    @staticmethod
    def init_gui():
        """
        MUST BE CALLED BEFORE ACCESSING ANY CLASS VARIABLES. Sets up the display window.
        """
        # Control window
        TestGUI.control_window = tk.Tk()
        TestGUI.control_window.title("Control Panel")
        TestGUI._set_window_geometry(TestGUI.control_window, left_side=True)
        TestGUI._disable_close_button(TestGUI.control_window)

        # Test display window (child of control)
        TestGUI.display_window = tk.Toplevel()
        TestGUI.display_window.title("Display")
        TestGUI.display_window.configure(background='black')
        TestGUI._set_window_geometry(TestGUI.display_window, left_side=False)
        TestGUI._disable_close_button(TestGUI.display_window)

        # Display canvas filling the entire display window
        TestGUI.display_canvas = tk.Canvas(TestGUI.display_window, width=400, height=400, bg='black')
        TestGUI.display_canvas.pack(expand=True, fill=tk.BOTH)

        # Test lifecycle buttons (child of control)
        frame = tk.Frame(TestGUI.control_window)
        frame.pack(side="bottom", pady=100)

        TestGUI.abort_button = tk.Button(frame, text="ABORT TEST", height=4, width=30, state="disabled",
                                         command=lambda: TestGUI.current_thread.abort())
        TestGUI.abort_button.pack(side="left")

        TestGUI.close_button = tk.Button(frame, text="EXIT TESTING", height=4, width=30,
                                         command=lambda: TestGUI._exit())
        TestGUI.close_button.pack(side="right")

        TestGUI.timer_label = tk.Label(TestGUI.control_window, text="Elapsed Time: 0.00 seconds", height=5, width=30)
        TestGUI.timer_label.pack()  # Pack the timer label into the control window
        TestGUI.timer_queue = Queue()  # Initialize a queue for communication between thread

        TestGUI._prompt_participant_info()

        state_save_path = os.path.join(config.SAVED_DATA_PATH, TestGUI.participant_ID, TestGUI.session_ID, "test_states.json")
        if os.path.isfile(state_save_path):
            print("Found saved test states.")
            try:
                # Read data from file:
                TestGUI.tests = json.load(open(state_save_path))
            except:
                print("Error reading saved test states.")

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
        if not TestGUI.tests.get(test_name):
            TestGUI.tests[test_name] = {'lambda': test_lambda, 'button': btn, 'trial': 0, 'completed': False}
            print("Added test: " + test_name)
        else:
            TestGUI.tests[test_name]['button'] = btn
            TestGUI.tests[test_name]['lambda'] = test_lambda

            test = TestGUI.tests[test_name]
            if test['completed']:
                btn.config(state="disabled", bg="green")
            print(f"Added test from saved state: {test_name} - Trial: {test['trial']}, Completed: {test['completed']}")

    @staticmethod
    def confirm_current_test() -> bool:
        """
        Run the test and prompt the user to confirm or deny the data.
        """
        # Confirm data
        TestGUI._confirm_data()

        # Reset the buttons
        TestGUI.close_button.config(state="normal")
        TestGUI.abort_button.config(state="disabled")

        for test_name, test_info in TestGUI.tests.items():
            if not test_info['completed']:
                test_info['button'].config(state="normal", bg="red")
            else:
                test_info['button'].config(state="disabled", bg="green")

        # Reset the timer
        TestGUI._reset_timer()

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

        # Initialize test start time
        TestGUI.test_start_time = time.time()  # Record the start time

        # Start the timer
        TestGUI.timer_thread = threading.Thread(target=TestGUI._update_timer)
        TestGUI.timer_thread.start()

        TestGUI.test_start_time = time.time()  # Record the start time

    @staticmethod
    def place_image(image):
        """
        Helper function to place an image in the middle of the display window. Returns the ID of the image object
        for destruction.

        :param image: The Tkinter image to place
        """
        if TestGUI.current_display_element is not None:
            TestGUI.destroy_current_element()

        x = TestGUI.display_canvas.winfo_width() // 2
        y = TestGUI.display_canvas.winfo_height() // 2
        TestGUI.current_display_element = TestGUI.display_canvas.create_image(x, y, anchor=tk.CENTER, image=image)

    @staticmethod
    def place_text(text):
        """
        Helper function to place text in the middle of the display window. Returns the ID of the text object
        for destruction.

        :param text: The text to place
        """
        if TestGUI.current_display_element is not None:
            TestGUI.destroy_current_element()

        x = TestGUI.display_canvas.winfo_width() // 2
        y = TestGUI.display_canvas.winfo_height() // 2
        TestGUI.current_display_element = TestGUI.display_canvas.create_text(x, y, anchor=tk.CENTER, text=text,
                                                                             fill='white', font='Helvetica 25 bold')

    @staticmethod
    def destroy_current_element():
        """
        Helper function to remove the current element (text or image) from the display canvas.
        """
        if TestGUI.current_display_element is not None:
            TestGUI.display_canvas.delete(TestGUI.current_display_element)

    @staticmethod
    def _update_timer():
        """
        Update the timer label with the elapsed time.
        """
        # TODO Instead message could be initialized above the while loop and the condition could be
        #  while message != "stop". It accomplishes the same thing but makes it a bit more clear as
        #  to when the loop quits - Feedback from Matt L., needs to be tested for thread safety first
        while True:
            # Check for messages in the queue
            try:
                message = TestGUI.timer_queue.get(block=False)
                if message == "stop":
                    # Stop the timer
                    break
                elif message == "reset":
                    # Reset the timer label
                    TestGUI.timer_label.config(text="Elapsed Time: 0.00 seconds")
            except:
                pass  # No messages in the queue, continue updating the timer

            # Update the timer label with the elapsed time
            elapsed_time = time.time() - TestGUI.test_start_time
            elapsed_seconds = int(elapsed_time)
            milliseconds = int((elapsed_time - elapsed_seconds) * 100)
            TestGUI.timer_label.config(text=f"Elapsed Time: {elapsed_seconds}.{milliseconds:02d} seconds")
            time.sleep(0.01)  # Update the label every 10 milliseconds

    @staticmethod
    def _stop_timer():
        """
        Stop the timer.
        """
        # Send a "stop" message to the timer thread
        TestGUI.timer_queue.put("stop")

    @staticmethod
    def _reset_timer():
        """
        Reset the timer label.
        """
        # Send a "reset" message to the timer thread
        TestGUI.timer_label.config(text="Elapsed Time: 0.00 seconds")
        TestGUI.timer_queue.put("reset")

    @staticmethod
    def _confirm_data():
        """
        Popup the data confirmation window to check if it should be accepted or rejected,
        without displaying graphs.
        """
        # Stop the timer
        TestGUI._stop_timer()

        popup = tk.Toplevel()
        popup.wm_title("Data Confirmation")
        TestGUI._disable_close_button(popup)
        popup.geometry("400x200")
        msg = tk.Label(popup, text="Confirm Test Data", font=("Arial", 12))
        msg.pack(pady=20)
        confirm_button = tk.Button(popup, text="Confirm", command=lambda: TestGUI._handle_confirm(popup, True))
        deny_button = tk.Button(popup, text="Deny", command=lambda: TestGUI._handle_confirm(popup, False))
        confirm_button.pack(side="left", padx=20, pady=20)
        deny_button.pack(side="right", padx=20, pady=20)
        popup.grab_set()
        TestGUI.control_window.wait_window(popup)

    @staticmethod
    def _handle_confirm(popup, confirmed):
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
    def _prompt_participant_info():
        """
        Creates a mandatory popup to prompt the user for the participant number and session,
        and sets TestGUI.participant_number and TestGUI.session to the result.
        Info that has to be collected: Participant:P001 Session:S001
        """

        popup = tk.Toplevel(TestGUI.control_window)
        TestGUI._disable_close_button(popup)
        popup.wm_title("Enter Participant Information")
        TestGUI.control_window.eval(f'tk::PlaceWindow {str(popup)} center')

        #variables for ensuring you can't do the same tests twice
        error_text = tk.Label(popup, text="Already exists", height=5, width=30, fg="red")
        exists = False

        participant = tk.StringVar(value="P001")
        session = tk.StringVar(value="S001")

        def submit():
            TestGUI.participant_ID = participant.get()
            TestGUI.session_ID = session.get()
            print(f"Participant: {TestGUI.participant_ID}, Session: {TestGUI.session_ID}")

            #ensuring that the session has not already been run
            state_save_path = os.path.join(config.SAVED_DATA_PATH, TestGUI.participant_ID, TestGUI.session_ID)
            if os.path.exists(state_save_path) and exists == False:
                exists = True
                error_text.pack()
            elif exists == True:
                pass
            else:
                popup.destroy()

        tk.Entry(popup, textvariable=participant).pack()
        tk.Entry(popup, textvariable=session).pack()

        submit_button = tk.Button(popup, text='Begin', command=submit)
        submit_button.pack()

        popup.grab_set()
        TestGUI.control_window.wait_window(popup)

    @staticmethod
    def _exit():
        """
        Helper function that handles the exit behavior of the GUI.
        """
        # Create save path if it doesn't exist
        state_save_path = os.path.join(config.SAVED_DATA_PATH, TestGUI.participant_ID, TestGUI.session_ID)
        if not os.path.exists(state_save_path):
            os.makedirs(state_save_path)
        state_save_path = os.path.join(state_save_path, "test_states.json")

        # Remove GUI-specific data (lambda, button) from subkeys
        keys_to_remove = ['button', 'lambda']
        for test in TestGUI.tests.keys():
            for key in keys_to_remove:
                if TestGUI.tests[test].get(key):
                    del TestGUI.tests[test][key]

        # Serialize test data into file:
        json.dump(TestGUI.tests, open(state_save_path, 'w'))
        print("Test data serialized to test_states.json")

        TestGUI.display_window.destroy()
        TestGUI.control_window.destroy()
        print("Exiting Data Collector")
        exit(0)

    @staticmethod
    def _disable_close_button(window):
        """
        Helper function that disables the close/X button of the specified window.

        :param window: The window to disable the closing of.
        """

        def disable_event():
            pass

        window.protocol("WM_DELETE_WINDOW", disable_event)

    @staticmethod
    def _set_window_geometry(window, left_side=True):
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
