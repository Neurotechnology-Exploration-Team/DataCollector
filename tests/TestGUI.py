import os.path
import tkinter as tk

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from postprocessing.NoiseReduction import butter_bandpass_filter
import config


class TestGUI:
    """
    Holds all logic relating to creating the GUI, adding buttons/windows, and the test confirmation window.
    """

    control_window = None
    display_window = None
    close_button = None

    # Setup test states: A dictionary with test name keys corresponding to sub-dictionaries with lambda, button,
    # trial_number, and completed parameters
    tests = {}
    current_test = None

    participant_ID = ""
    session_ID = ""

    @staticmethod
    def init_gui():
        """
        MUST BE CALLED BEFORE ACCESSING ANY CLASS VARIABLES. Sets up the display window.
        """
        TestGUI.control_window = tk.Tk()
        TestGUI.control_window.title("Control Panel")
        TestGUI.__set_window_geometry(TestGUI.control_window, left_side=True)
        TestGUI.disable_close_button(TestGUI.control_window)

        TestGUI.display_window = tk.Toplevel(TestGUI.control_window)
        TestGUI.display_window.title("Display")
        TestGUI.display_window.configure(background='black')
        TestGUI.__set_window_geometry(TestGUI.display_window, left_side=False)
        TestGUI.disable_close_button(TestGUI.display_window)

        TestGUI.close_button = tk.Button(TestGUI.control_window, text="EXIT TESTING", height=5, width=30)
        TestGUI.close_button.config(command=lambda: TestGUI.__exit())
        TestGUI.close_button.pack(side="bottom", pady=100)

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
    def confirm_current_test(test_data_path: str) -> bool:
        """
        Run the test and prompt the user to confirm or deny the data.

        :param test_data_path: The path to the current test data FOLDER.
        """
        # Confirm data
        TestGUI.__show_data_and_confirm(test_data_path)

        TestGUI.close_button.config(state="normal")
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
        return TestGUI.tests[TestGUI.current_test]['completed']

    @staticmethod
    def start_test(test_name):
        """
        A function to disable buttons while a test is running.

        :param test_name: The name of the current test running (to enable the indicator).
        """
        # Disable all buttons
        TestGUI.close_button.config(state="disabled")

        for test in TestGUI.tests.keys():
            TestGUI.tests[test]['button'].config(state="disabled")

        # Indicate current test
        TestGUI.current_test = test_name
        TestGUI.tests[TestGUI.current_test]['button'].config(bg="yellow")

    #
    # HELPER METHODS
    #

    @staticmethod
    def __show_data_and_confirm(test_data_path: str):
        """
        Popup the data confirmation window and check if it should be accepted or rejected.
        If enabled for collection, EEG and accelerometer graphs will be displayed.

        :param test_data_path: The path to the test data CSV.
        """
        # Setup the window and canvas
        popup = tk.Toplevel()
        popup.wm_title("Data Confirmation")
        TestGUI.disable_close_button(popup)

        if os.name == "posix":  # Needs to be different for unix
            popup.attributes('-fullscreen')
        else:
            popup.state('zoomed')

        canvas = tk.Canvas(popup)
        scrollbar = tk.Scrollbar(popup, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Make it scrollable so we don't have to click the tiny scrollbar
        canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1 * (event.delta / 120)), "units"))

        # Read in and merge all data from the trial into a single dataframe
        # This should ignore NaN values, so graphs will not go to zero unless value is actually zero
        frames = []
        for stream_type, enabled in config.SUPPORTED_STREAMS.items():
            if enabled and stream_type != 'FFT':
                frames.append(pd.read_csv(os.path.join(test_data_path, f"{stream_type}_data.csv")))
        data_df = pd.concat(frames, axis=1)

        # Figure out how many graphs we can fit on the screen
        screen_width = popup.winfo_screenwidth()
        graphs_per_row = screen_width // config.WIDTH_PER_GRAPH

        if graphs_per_row == 0:
            graphs_per_row = 1

        # Loop through each EEG and draw the graphs
        if config.SUPPORTED_STREAMS['EEG']:
            idx = 0
            for idx, col in enumerate(data_df.filter(like='EEG')):
                fig, ax = plt.subplots(figsize=(config.WIDTH_PER_GRAPH / config.HEIGHT_PER_GRAPH, 3))
                filtered_data = butter_bandpass_filter(data_df[col], order=6)
                ax.plot(filtered_data)
                ax.set_title(f'{col} Data')
                FigureCanvasTkAgg(fig, master=scrollable_frame).get_tk_widget().grid(row=idx // graphs_per_row,
                                                                                     column=idx % graphs_per_row)

        # Now draw the accelerometer graph at the end
        if config.SUPPORTED_STREAMS['Accelerometer']:
            accel_data = data_df.filter(like='Accelerometer').mean(axis=1)
            fig2, ax2 = plt.subplots(
                figsize=(config.WIDTH_PER_GRAPH / config.HEIGHT_PER_GRAPH, 3))
            ax2.plot(accel_data)
            ax2.set_title('Accelerometer Data')
            FigureCanvasTkAgg(fig2, master=scrollable_frame).get_tk_widget().grid(row=(idx + 1) // graphs_per_row,
                                                                                  column=(idx + 1) % graphs_per_row)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def confirm_data():
            popup.destroy()
            TestGUI.tests[TestGUI.current_test]['completed'] = True

        # Create buttons to accept and deny the data
        confirm_button = tk.Button(scrollable_frame, text="Confirm Data", command=lambda: confirm_data())
        confirm_button.grid(row=(idx + 2) // graphs_per_row, column=0, pady=10)

        deny_button = tk.Button(scrollable_frame, text="Deny Data", command=lambda: popup.destroy())
        deny_button.grid(row=(idx + 2) // graphs_per_row, column=1, pady=10)

        # Force popup to be on top & halt program execution
        popup.grab_set()
        TestGUI.control_window.wait_window(popup)

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
