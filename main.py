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
import postProcessing
import time

from LSL import LSL

# Boolean constant to determine screen mode
FULL_SCREEN_MODE = False  # Set to True for full-screen, False for split-screen

# Data list to store timestamps and labels
collected_data = []

# Folder for CSV downloads
CSV_FOLDER = "./csv_downloads"                            # Folder that the CSVs will be saved to
COLLECTED_DATA_PATH = f'{CSV_FOLDER}/collected_data.csv'  # Path to save LSL data to
EVENT_DATA_PATH = f'{CSV_FOLDER}/event_data.csv'          # Path to save event data to
LABELED_DATA_PATH = f'{CSV_FOLDER}/labeled_data.csv'      # Path to save processed, labeled data to

def run_test(test_name, btn, lsl: LSL):
    global current_test_thread, current_test_button
    current_test_button = btn
    # Disable buttons
    for button in test_buttons.values():
        button.config(state="disabled")

    # Dynamic import
    test_module = importlib.import_module(f"tests.{test_name}")

    # Running the test in a separate thread
    current_test_thread = threading.Thread(
        target=test_module.run,
        args=(display_window, record_timestamp, enable_buttons, lsl, COLLECTED_DATA_PATH))
    current_test_thread.start()


def record_timestamp(event_name):
    timestamp = datetime.now()
    collected_data.append((event_name, timestamp))
    print(f"{event_name}: {timestamp}")


def enable_buttons():
    for button in test_buttons.values():
        button.config(state="normal")
        save_to_csv()
        time.sleep(1)
        postProcessing.label_data_based_on_events(COLLECTED_DATA_PATH, EVENT_DATA_PATH, LABELED_DATA_PATH)
        time.sleep(1)
        show_data_and_confirm()  # Show the popup for data confirmation
    # Prompt for test acceptance
    if messagebox.askyesno("Test Complete", "Do you want to accept this test?"):

        current_test_button.config(bg="green")

    else:
        current_test_button.config(bg="red")
        collected_data.clear()  # Clear data if test is rejected
    for button in test_buttons.values():
        button.config(state="normal")


def save_to_csv():
    if not collected_data:
        return

    with open(EVENT_DATA_PATH, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Event", "Timestamp"])
        for data in collected_data:
            writer.writerow(data)
    collected_data.clear()
    print(f"Event Data saved to {EVENT_DATA_PATH}")


def set_window_geometry(window, left_side=True):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    if FULL_SCREEN_MODE:
        window.geometry(f"{screen_width}x{screen_height}+0+0")
    else:
        width = screen_width // 2
        x = 0 if left_side else width
        window.geometry(f"{width}x{screen_height}+{x}+0")


def show_data_and_confirm():  # TODO broken?
    # Load the data
    data_df = pd.read_csv(LABELED_DATA_PATH)

    # Create a new Tkinter window
    popup = tk.Toplevel()
    popup.wm_title("Data Confirmation")

    # Create a canvas with a scrollbar
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

    # Loop to create plots for EEG and Accelerometer data
    for col in data_df.filter(like='EEG'):
        fig, ax = plt.subplots()
        ax.plot(data_df[col])
        ax.set_title(f'{col} Data')
        FigureCanvasTkAgg(fig, master=scrollable_frame).get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    accel_data = data_df.filter(like='Accelerometer').mean(axis=1)
    fig2, ax2 = plt.subplots()
    ax2.plot(accel_data)
    ax2.set_title('Accelerometer Data')
    FigureCanvasTkAgg(fig2, master=scrollable_frame).get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Pack the canvas and scrollbar in the window
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Add a confirmation button
    confirm_button = tk.Button(scrollable_frame, text="Confirm Data", command=popup.destroy)
    confirm_button.pack()

    popup.mainloop()


if __name__ == '__main__':
    # Make output directory
    os.makedirs(CSV_FOLDER, exist_ok=True)

    # Initialize LSL streams
    lsl = LSL()

    # Control window
    control_window = tk.Tk()
    control_window.title("Control Panel")
    set_window_geometry(control_window, left_side=True)

    # Display window
    display_window = tk.Toplevel(control_window)
    display_window.title("Display")
    set_window_geometry(display_window, left_side=False)

    # Importing test names from the tests directory
    test_directory = 'tests'
    test_names = [filename.split('.')[0] for filename in os.listdir(test_directory) if filename.endswith('.py')]


    def create_lambda(test_name, btn):
        return lambda: run_test(test_name, btn, lsl)


    # Creating buttons for each test
    test_buttons = {}
    for test_name in test_names:
        btn = tk.Button(control_window, text=test_name)
        btn.config(command=create_lambda(test_name, btn))
        btn.pack()
        test_buttons[test_name] = btn

    control_window.mainloop()
