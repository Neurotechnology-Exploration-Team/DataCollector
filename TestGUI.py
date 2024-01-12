import time
import tkinter as tk
from tkinter import messagebox

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import config
from LSL import EventLogger
from post_processing import label_data_based_on_events


class TestGUI:
    def __init__(self):
        self.control_window = tk.Tk()
        self.control_window.title("Control Panel")
        TestGUI.set_window_geometry(self.control_window, left_side=True)

        self.display_window = tk.Toplevel(self.control_window)
        self.display_window.title("Display")
        TestGUI.set_window_geometry(self.display_window, left_side=False)

        self.test_buttons = {}
        self.current_test_thread = None
        self.current_test_button = None

    def enable_buttons(self):
        """
        Run the test and prompt the user to confirm or deny the data
        """
        for button in self.test_buttons.values():
            button.config(state="normal")
            EventLogger.save_to_csv()
            time.sleep(1)

            # Process data
            label_data_based_on_events()

            time.sleep(1)
            TestGUI.show_data_and_confirm()

        # Prompt for test acceptance
        if messagebox.askyesno("Test Complete", "Do you want to accept this test?"):
            self.current_test_button.config(bg="green")

        else:
            # If the data is rejected then we want to clear everything collected
            self.current_test_button.config(bg="red")
            EventLogger.clear_data()

        # Reset the buttons
        for button in self.test_buttons.values():
            button.config(state="normal")

    def disable_buttons(self):
        for button in self.test_buttons.values():
            button.config(state="disabled")

    @staticmethod
    def show_data_and_confirm():
        """
        Popup the data confirmation window and check if it should be accepted or rejected
        """
        # Setup the window and canvas
        popup = tk.Toplevel()
        popup.wm_title("Data Confirmation")
        popup.wm_state('zoomed')

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
        TestGUI.enable_scroll(canvas)

        data_df = pd.read_csv(config.LABELED_DATA_PATH)

        # Figure out how many graphs we can fit on the screen
        screen_width = popup.winfo_screenwidth()
        graphs_per_row = screen_width // config.WIDTH_PER_GRAPH

        if graphs_per_row == 0:
            graphs_per_row = 1

        # Loop through each EEG and draw the graphs
        idx = 0
        for idx, col in enumerate(data_df.filter(like='EEG')):
            fig, ax = plt.subplots(figsize=(config.WIDTH_PER_GRAPH / config.HEIGHT_PER_GRAPH, 3))
            ax.plot(data_df[col])
            ax.set_title(f'{col} Data')
            FigureCanvasTkAgg(fig, master=scrollable_frame).get_tk_widget().grid(row=idx // graphs_per_row,
                                                                                 column=idx % graphs_per_row)

        # Now draw the accelerometer graph at the end
        accel_data = data_df.filter(like='Accelerometer').mean(axis=1)
        fig2, ax2 = plt.subplots(
            figsize=(config.WIDTH_PER_GRAPH / config.HEIGHT_PER_GRAPH, 3))
        ax2.plot(accel_data)
        ax2.set_title('Accelerometer Data')
        FigureCanvasTkAgg(fig2, master=scrollable_frame).get_tk_widget().grid(row=(idx + 1) // graphs_per_row,
                                                                              column=(idx + 1) % graphs_per_row)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Create buttons to accept and deny the data
        confirm_button = tk.Button(scrollable_frame, text="Confirm Data", command=popup.destroy)
        confirm_button.grid(row=(idx + 2) // graphs_per_row, column=0, pady=10)

        deny_button = tk.Button(scrollable_frame, text="Deny Data", command=lambda: TestGUI.deny_data(popup))
        deny_button.grid(row=(idx + 2) // graphs_per_row, column=1, pady=10)

        popup.mainloop()

    @staticmethod
    def deny_data(popup):
        """
        Run if the deny button is pressed

        :param popup: Popup window which must be closed
        """
        # Close window and then clear all the data
        popup.destroy()
        EventLogger.clear_data()

    @staticmethod
    def enable_scroll(canvas):
        """
        Function to enable scrolling using the mouse wheel

        NOTE: There may be a better solution for this, this is what I could find easily online
        """
        canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1 * (event.delta / 120)), "units"))

    @staticmethod
    def set_window_geometry(window, left_side=True):
        """
        Figure out size for a window and align it according to left_side

        :param window: Window passed from TKinter
        :param left_side: If it should be aligned on the left side or right
        """
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        if config.FULL_SCREEN_MODE:
            window.geometry(f"{screen_width}x{screen_height}+0+0")
        else:
            width = screen_width // 2
            x = 0 if left_side else width
            window.geometry(f"{width}x{screen_height}+{x}+0")