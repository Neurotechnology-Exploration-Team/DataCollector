import os
import tkinter as tk
import json

import config
import timer
from threading import Thread

"""
Holds all logic relating to creating the GUI, adding buttons/windows, and the test confirmation window.

This acts as an all-in-one test controller and GUI manager.
"""

# Window variables
control_window = tk.Tk()
display_window = tk.Toplevel()
# The canvas on the display window to display images/text
display_canvas = tk.Canvas(display_window, width=400, height=400, bg='black')
close_button: tk.Button = None
abort_button: tk.Button = None

current_display_element: int = None  # The ID of the current element being displayed on display_canvas

# Setup test states: A dictionary with test name keys corresponding to sub-dictionaries with lambda, button,
# trial_number, and completed parameters
tests = {}
current_thread: Thread = None

participant_ID = ""
session_ID = ""


def init_gui():
    """
    MUST BE CALLED BEFORE ACCESSING ANY CLASS VARIABLES. Sets up the display window.
    """
    global control_window, display_window, display_canvas, abort_button, close_button, tests, participant_ID, session_ID

    # Control window
    control_window.title("Control Panel")
    _set_window_geometry(control_window, left_side=True)
    _disable_close_button(control_window)

    # Test display window (child of control)
    display_window.title("Display")
    display_window.configure(background='black')
    _set_window_geometry(display_window, left_side=False)
    _disable_close_button(display_window)

    # Display canvas filling the entire display window
    display_canvas.pack(expand=True, fill=tk.BOTH)

    # Test lifecycle buttons (child of control)
    frame = tk.Frame(control_window)
    frame.pack(side="bottom", pady=100)

    def abort_thread():
        if current_thread:
            current_thread.abort()

    abort_button = tk.Button(frame, text="ABORT TEST", height=4, width=30, state="disabled",
                             command=abort_thread)
    abort_button.pack(side="left")

    close_button = tk.Button(frame, text="EXIT TESTING", height=4, width=30, command=_exit)
    close_button.pack(side="right")

    timer_label = tk.Label(control_window, text="Elapsed Time: 0.00 seconds", height=5, width=30)
    timer.init_label(timer_label)  # Initialize timer with new label
    timer_label.pack()  # Pack the timer label into the control window

    _prompt_participant_info()

    state_save_path = os.path.join(config.SAVED_DATA_PATH, participant_ID, session_ID,
                                   "test_states.json")
    if os.path.isfile(state_save_path):
        print("Found saved test states.")
        try:
            # Read data from file:
            tests = json.load(open(state_save_path))
        except:
            print("Error reading saved test states.")


def add_test(test_name: str, test_lambda):
    """
    Adds a button to the test window with its name and function to run.

    :param test_name: The name of the test that the button will be assigned to.
    :param test_lambda: The function that the test will be ran with (no arguments).
    """
    global tests

    # Configure button
    btn = tk.Button(control_window, text=test_name)
    btn.config(command=test_lambda, bg='red')
    btn.pack()

    # Configure test state
    if not tests.get(test_name):
        tests[test_name] = {'lambda': test_lambda, 'button': btn, 'trial': 0, 'completed': False}
        print("Added test: " + test_name)
    else:
        tests[test_name]['button'] = btn
        tests[test_name]['lambda'] = test_lambda

        test = tests[test_name]
        if test['completed']:
            btn.config(state="disabled", bg="green")
        print(f"Added test from saved state: {test_name} - Trial: {test['trial']}, Completed: {test['completed']}")


def confirm_current_test() -> bool:
    """
    Run the test and prompt the user to confirm or deny the data.
    """
    global close_button, abort_button, tests, current_thread

    # Confirm data
    _confirm_data()

    # Reset the buttons
    close_button.config(state="normal")
    abort_button.config(state="disabled")

    for test_name, test_info in tests.items():
        if not test_info['completed']:
            test_info['button'].config(state="normal", bg="red")
        else:
            test_info['button'].config(state="disabled", bg="green")

    # Reset the timer
    timer.reset()

    # Return true if test is complete
    return tests[current_thread.name]['completed']


def start_test(test_thread):
    """
    A function to disable buttons while a test is running.

    :param test_thread: The thread object of the current test running (to enable the indicator).
    """
    global close_button, abort_button, current_thread

    # Disable all buttons
    close_button.config(state="disabled")
    abort_button.config(state="normal")

    for test in tests.keys():
        tests[test]['button'].config(state="disabled")

    # Indicate current test
    current_thread = test_thread
    tests[current_thread.name]['button'].config(bg="yellow")

    timer.start()


def place_image(image):
    """
    Helper function to place an image in the middle of the display window. Returns the ID of the image object
    for destruction.

    :param image: The Tkinter image to place
    """
    global current_display_element, display_canvas

    if current_display_element is not None:
        destroy_current_element()

    x = display_canvas.winfo_width() // 2
    y = display_canvas.winfo_height() // 2
    current_display_element = display_canvas.create_image(x, y, anchor=tk.CENTER, image=image)


def place_text(text):
    """
    Helper function to place text in the middle of the display window. Returns the ID of the text object
    for destruction.

    :param text: The text to place
    """
    global current_display_element, display_canvas

    if current_display_element is not None:
        destroy_current_element()

    x = display_canvas.winfo_width() // 2
    y = display_canvas.winfo_height() // 2
    current_display_element = display_canvas.create_text(x, y, anchor=tk.CENTER, text=text, fill='white',
                                                         font='Helvetica 25 bold')


def destroy_current_element():
    """
    Helper function to remove the current element (text or image) from the display canvas.
    """
    global current_display_element, display_canvas

    if current_display_element is not None:
        display_canvas.delete(current_display_element)


def _confirm_data():
    """
    Popup the data confirmation window to check if it should be accepted or rejected,
    without displaying graphs.
    """
    global control_window

    # Stop the timer
    timer.stop()

    popup = tk.Toplevel()
    popup.wm_title("Data Confirmation")
    _disable_close_button(popup)
    popup.geometry("400x200")
    msg = tk.Label(popup, text="Confirm Test Data", font=("Arial", 12))
    msg.pack(pady=20)
    confirm_button = tk.Button(popup, text="Confirm", command=lambda: _handle_confirm(popup, True))
    deny_button = tk.Button(popup, text="Deny", command=lambda: _handle_confirm(popup, False))
    confirm_button.pack(side="left", padx=20, pady=20)
    deny_button.pack(side="right", padx=20, pady=20)
    popup.grab_set()
    control_window.wait_window(popup)


def _handle_confirm(popup, confirmed):
    """
    Handle the confirmation or denial of data.
    """
    global tests, current_thread

    if confirmed:
        print("Data confirmed.")
    else:
        print("Data denied.")
    tests[current_thread.name]['completed'] = confirmed
    popup.destroy()
    for test_name, test_info in tests.items():
        if not test_info['completed']:
            test_info['button'].config(state="normal", bg="red")
        else:
            test_info['button'].config(state="disabled", bg="green")


def _prompt_participant_info():
    """
    Creates a mandatory popup to prompt the user for the participant number and session,
    and sets TestGUI.participant_number and TestGUI.session to the result.
    Info that has to be collected: Participant:P001 Session:S001
    """
    global control_window

    popup = tk.Toplevel(control_window)
    _disable_close_button(popup)
    popup.wm_title("Enter Participant Information")
    control_window.eval(f'tk::PlaceWindow {str(popup)} center')

    participant = tk.StringVar(value="P001")
    session = tk.StringVar(value="S001")

    def submit():
        set_IDs(participant.get(), session.get())
        print(f"Participant: {participant_ID}, Session: {session_ID}")

        popup.destroy()

    tk.Entry(popup, textvariable=participant).pack()
    tk.Entry(popup, textvariable=session).pack()

    submit_button = tk.Button(popup, text='Begin', command=submit)
    submit_button.pack()

    popup.grab_set()
    control_window.wait_window(popup)


def _exit():
    """
    Helper function that handles the exit behavior of the GUI.
    """
    global tests, display_window, control_window, participant_ID, session_ID
    state_save_path = os.path.join(config.SAVED_DATA_PATH, participant_ID, session_ID,
                                   "test_states.json")

    # Remove GUI-specific data (lambda, button) from subkeys
    keys_to_remove = ['button', 'lambda']
    for test in tests.keys():
        for key in keys_to_remove:
            if tests[test].get(key):
                del tests[test][key]

    # Serialize test data into file:
    try:
        json.dump(tests, open(state_save_path, 'w'))
        print("Test status data serialized to test_states.json")
    except:
        print(f"Error serializing test status data to {state_save_path}")

    display_window.destroy()
    control_window.destroy()
    print("Exiting Data Collector")
    exit(0)


def set_IDs(pid, sid):
    """
    Weird helper method, otherwise there are issues with the global variables.
    """
    # TODO find a less hacky fix 💀
    global participant_ID, session_ID
    participant_ID = pid
    session_ID = sid


def _disable_close_button(window):
    """
    Helper function that disables the close/X button of the specified window.

    :param window: The window to disable the closing of.
    """

    def disable_event():
        pass

    window.protocol("WM_DELETE_WINDOW", disable_event)


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


def get_trial_number(test_name: str) -> int:
    return tests[test_name]["trial"]


def increment_trial_number(test_name: str) -> None:
    tests[test_name]["trial"] += 1
