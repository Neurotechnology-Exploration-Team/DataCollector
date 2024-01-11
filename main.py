import tkinter as tk
import importlib
import os
from datetime import datetime
import threading
import csv
from tkinter import messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from post_processing import label_data_based_on_events
import time

from LSL import LSL


class DataCollectorApp:
    """
    Class as a collection of all functions that interact with the test GUI
    """
    FULL_SCREEN_MODE = False
    DATA_PATH = "./csv_downloads"
    COLLECTED_DATA_PATH = f'{DATA_PATH}/collected_data.csv'
    EVENT_DATA_PATH = f'{DATA_PATH}/event_data.csv'
    LABELED_DATA_PATH = f'{DATA_PATH}/labeled_data.csv'
    collected_data = []
    test_buttons = {}

    WIDTH_PER_GRAPH = 400
    HEIGHT_PER_GRAPH = 80

    @staticmethod
    def run_test(test_name, btn, lsl: LSL, display_window):
        """
        Connect to lsl and run the test in a thread

        :param test_name: Name of test being run
        :param btn: The test being run (which button was pushed)
        :param lsl: LSL connection to openBCI
        :param display_window: Window from TKinter
        """
        global current_test_thread, current_test_button
        current_test_button = btn

        for button in DataCollectorApp.test_buttons.values():
            button.config(state="disabled")

        test_module = importlib.import_module(f"tests.{test_name}")

        current_test_thread = threading.Thread(
            target=test_module.run,
            args=(display_window, DataCollectorApp.record_timestamp, DataCollectorApp.enable_buttons, lsl, DataCollectorApp.COLLECTED_DATA_PATH)
        )
        current_test_thread.start()

    @staticmethod
    def record_timestamp(event_name):
        """
        Record the time the data was collected along with the event

        :param event_name: Event that was collected
        """
        timestamp = datetime.now()
        DataCollectorApp.collected_data.append((event_name, timestamp))
        print(f"{event_name}: {timestamp}")

    @staticmethod
    def enable_buttons():
        """
        Run the test and prompt the user to confirm or deny the data
        """
        for button in DataCollectorApp.test_buttons.values():
            button.config(state="normal")
            DataCollectorApp.save_to_csv()
            time.sleep(1)

            # Process data
            label_data_based_on_events(DataCollectorApp.COLLECTED_DATA_PATH, DataCollectorApp.EVENT_DATA_PATH, DataCollectorApp.LABELED_DATA_PATH)

            time.sleep(1)
            DataCollectorApp.show_data_and_confirm()

        # Prompt for test acceptance
        if messagebox.askyesno("Test Complete", "Do you want to accept this test?"):
            current_test_button.config(bg="green")

        else:
            # If the data is rejected then we want to clear everything collected
            current_test_button.config(bg="red")
            DataCollectorApp.collected_data.clear()

        # Reset the buttons
        for button in DataCollectorApp.test_buttons.values():
            button.config(state="normal")

    @staticmethod
    def save_to_csv() -> bool:
        """
        Write all data to the csv files

        :return: If the writing was successful
        """
        if not DataCollectorApp.collected_data:
            return False

        # Wrap it to catch any file issues
        try:
            with open(DataCollectorApp.EVENT_DATA_PATH, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Event", "Timestamp"])
                for data in DataCollectorApp.collected_data:
                    writer.writerow(data)
        except Exception:
            return False

        DataCollectorApp.collected_data.clear()
        print(f"Event Data saved to {DataCollectorApp.EVENT_DATA_PATH}")

        return True

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
        DataCollectorApp.enable_scroll(canvas)

        data_df = pd.read_csv(DataCollectorApp.LABELED_DATA_PATH)

        # Figure out how many graphs we can fit on the screen
        screen_width = popup.winfo_screenwidth()
        graphs_per_row = screen_width // DataCollectorApp.WIDTH_PER_GRAPH

        if graphs_per_row == 0:
            graphs_per_row = 1

        # Loop through each EEG and draw the graphs
        idx = 0
        for idx, col in enumerate(data_df.filter(like='EEG')):
            fig, ax = plt.subplots(figsize=(DataCollectorApp.WIDTH_PER_GRAPH / DataCollectorApp.HEIGHT_PER_GRAPH, 3))
            ax.plot(data_df[col])
            ax.set_title(f'{col} Data')
            FigureCanvasTkAgg(fig, master=scrollable_frame).get_tk_widget().grid(row=idx // graphs_per_row,
                                                                                 column=idx % graphs_per_row)

        # Now draw the accelerometer graph at the end
        accel_data = data_df.filter(like='Accelerometer').mean(axis=1)
        fig2, ax2 = plt.subplots(
            figsize=(DataCollectorApp.WIDTH_PER_GRAPH / DataCollectorApp.HEIGHT_PER_GRAPH, 3))
        ax2.plot(accel_data)
        ax2.set_title('Accelerometer Data')
        FigureCanvasTkAgg(fig2, master=scrollable_frame).get_tk_widget().grid(row=(idx + 1) // graphs_per_row,
                                                                              column=(idx + 1) % graphs_per_row)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Create buttons to accept and deny the data
        confirm_button = tk.Button(scrollable_frame, text="Confirm Data", command=popup.destroy)
        confirm_button.grid(row=(idx + 2) // graphs_per_row, column=0, pady=10)

        deny_button = tk.Button(scrollable_frame, text="Deny Data", command=lambda: DataCollectorApp.deny_data(popup))
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
        DataCollectorApp.collected_data.clear()

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

        if DataCollectorApp.FULL_SCREEN_MODE:
            window.geometry(f"{screen_width}x{screen_height}+0+0")
        else:
            width = screen_width // 2
            x = 0 if left_side else width
            window.geometry(f"{width}x{screen_height}+{x}+0")

    @staticmethod
    def main():
        """
        Main function for collecting data using the tkinter application
        """
        os.makedirs(DataCollectorApp.DATA_PATH, exist_ok=True)
        lsl = LSL()

        control_window = tk.Tk()
        control_window.title("Control Panel")
        DataCollectorApp.set_window_geometry(control_window, left_side=True)

        display_window = tk.Toplevel(control_window)
        display_window.title("Display")
        DataCollectorApp.set_window_geometry(display_window, left_side=False)

        test_directory = 'tests'
        test_names = [filename.split('.')[0] for filename in os.listdir(test_directory) if filename.endswith('.py')]

        def create_lambda(test_name, btn, display_window):
            return lambda: DataCollectorApp.run_test(test_name, btn, lsl, display_window)

        DataCollectorApp.test_buttons = {}
        for test_name in test_names:
            btn = tk.Button(control_window, text=test_name)
            btn.config(command=create_lambda(test_name, btn, display_window))
            btn.pack()
            DataCollectorApp.test_buttons[test_name] = btn

        control_window.mainloop()


if __name__ == '__main__':
    DataCollectorApp.main()
