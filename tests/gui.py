import tkinter as tk


def set_window_geometry(window, left_side=True):
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


def disable_close_button(window):
    """
    Helper function that disables the close/X button of the specified window.

    :param window: The window to disable the closing of.
    """

    def disable_event():
        pass

    window.protocol("WM_DELETE_WINDOW", disable_event)


class TestGUI:
    """
    Holds all logic relating to creating the GUI, adding buttons/windows, and the test confirmation window.

    This acts as an all-in-one test controller and GUI manager.
    """

    def __init__(self, exit_fn, abort_fn):
        # Control window
        self.control_window = tk.Tk()
        self.control_window.title("Control Panel")
        set_window_geometry(self.control_window, left_side=True)
        disable_close_button(self.control_window)

        # Test display window (child of control)
        self.display_window = tk.Toplevel()
        self.display_window.title("Display")
        self.display_window.configure(background='black')
        set_window_geometry(self.display_window, left_side=False)
        disable_close_button(self.display_window)

        # The canvas on the display window to display images/text
        self.display_canvas = tk.Canvas(self.display_window, width=400, height=400, bg='black')
        self.display_canvas.pack(expand=True, fill=tk.BOTH)

        # Test lifecycle buttons (child of control)
        frame = tk.Frame(self.control_window)
        frame.pack(side="bottom", pady=100)

        self.close_button = tk.Button(frame, text="EXIT TESTING", height=4, width=30, command=exit_fn)
        self.abort_button = tk.Button(frame, text="ABORT TEST", height=4, width=30, state="disabled", command=abort_fn)

        self.close_button.pack(side="right")
        self.abort_button.pack(side="left")

        self.current_display_element = None  # The ID of the current element being displayed on display_canvas

        self.buttons = {}

        self.timer_label = tk.Label(self.control_window, text="Elapsed Time: 0.00 seconds", height=5, width=30)
        self.timer_label.pack()  # Pack the timer label into the control window

        self.prompt_participant_info()

    def add_test(self, test_name: str, test_lambda):
        """
        Adds a button to the test window with its name and function to run.

        :param test_name: The name of the test that the button will be assigned to.
        :param test_lambda: The function that the test will be ran with (no arguments).
        """
        # Configure button
        btn = tk.Button(self.control_window, text=test_name)
        btn.config(command=test_lambda, bg='red')
        btn.pack()
        self.buttons[test_name] = btn

    def disable_buttons(self, current_test_name):
        # Disable all buttons
        self.close_button.config(state="disabled")
        self.abort_button.config(state="normal")

        for btn in self.buttons.values():
            btn.config(state="disabled")

        # Indicate current test
        self.buttons[current_test_name].config(bg="yellow")

    def update_buttons(self, completed_test_names):
        # Reset the buttons
        self.close_button.config(state="normal")
        self.abort_button.config(state="disabled")

        for name, btn in self.buttons.items():
            if name not in completed_test_names:
                btn.config(state="normal", bg="red")
            else:
                btn.config(state="disabled", bg="green")

    def place_image(self, image):
        """
        Helper function to place an image in the middle of the display window. Returns the ID of the image object
        for destruction.

        :param image: The Tkinter image to place
        """
        if TestGUI.current_display_element is not None:
            self.destroy_current_element()

        x = self.display_canvas.winfo_width() // 2
        y = self.display_canvas.winfo_height() // 2
        TestGUI.current_display_element = self.display_canvas.create_image(x, y, anchor=tk.CENTER, image=image)

    def place_text(self, text):
        """
        Helper function to place text in the middle of the display window. Returns the ID of the text object
        for destruction.

        :param text: The text to place
        """
        if TestGUI.current_display_element is not None:
            self.destroy_current_element()

        x = self.display_canvas.winfo_width() // 2
        y = self.display_canvas.winfo_height() // 2
        TestGUI.current_display_element = self.display_canvas.create_text(x, y, anchor=tk.CENTER, text=text,
                                                                             fill='white', font='Helvetica 25 bold')

    def destroy_current_element(self):
        """
        Helper function to remove the current element (text or image) from the display canvas.
        """
        if self.current_display_element is not None:
            self.display_canvas.delete(self.current_display_element)

    def confirm_data(self):
        """
        Popup the data confirmation window to check if it should be accepted or rejected,
        without displaying graphs.
        """
        popup = tk.Toplevel()
        popup.wm_title("Data Confirmation")
        disable_close_button(popup)
        popup.geometry("400x200")
        msg = tk.Label(popup, text="Confirm Test Data", font=("Arial", 12))
        msg.pack(pady=20)

        confirmed = None

        def handle_confirm(popup, is_confirmed):
            nonlocal confirmed
            popup.destroy()
            confirmed = is_confirmed

        confirm_button = tk.Button(popup, text="Confirm", command=lambda: handle_confirm(popup, True))
        deny_button = tk.Button(popup, text="Deny", command=lambda: handle_confirm(popup, False))
        confirm_button.pack(side="left", padx=20, pady=20)
        deny_button.pack(side="right", padx=20, pady=20)
        popup.grab_set()
        self.control_window.wait_window(popup)

        return confirmed

    def prompt_participant_info(self):
        """
        Creates a mandatory popup to prompt the user for the participant number and session,
        and sets TestGUI.participant_number and TestGUI.session to the result.
        Info that has to be collected: Participant:P001 Session:S001
        """

        popup = tk.Toplevel(self.control_window)
        disable_close_button(popup)
        popup.wm_title("Enter Participant Information")
        self.control_window.eval(f'tk::PlaceWindow {str(popup)} center')

        participant = tk.StringVar(value="P001")
        session = tk.StringVar(value="S001")

        pid = "XX"
        sid = "XX"

        def submit():
            nonlocal pid, sid
            pid = participant.get()
            sid = session.get()
            # print(f"Participant: {pid}, Session: {sid}")

            popup.destroy()

        tk.Entry(popup, textvariable=participant).pack()
        tk.Entry(popup, textvariable=session).pack()

        submit_button = tk.Button(popup, text='Begin', command=submit)
        submit_button.pack()

        popup.grab_set()
        self.control_window.wait_window(popup)

        return pid, sid

    def exit_gui(self):
        """
        Helper function that handles the exit behavior of the GUI.
        """
        self.display_window.destroy()
        self.control_window.destroy()

