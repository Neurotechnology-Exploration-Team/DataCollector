
import tkinter as tk
import importlib
import os
from datetime import datetime
import threading
import csv
from tkinter import messagebox
import lsl
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import postProcessing
import time
folder = "./csv_downloads/"

# Boolean constant to determine screen mode
FULL_SCREEN_MODE = False  # Set to True for full-screen, False for split-screen

# Data list to store timestamps and labels
collected_data = []

# Folder for CSV downloads
csv_folder = "csv_downloads"
os.makedirs(csv_folder, exist_ok=True)

def run_test(test_name, btn):
    global current_test_thread, current_test_button
    current_test_button = btn
    # Disable buttons
    for button in test_buttons.values():
        button.config(state="disabled")

    # Dynamic import
    test_module = importlib.import_module(f"tests.{test_name}")
    
    # Running the test in a separate thread
    current_test_thread = threading.Thread(target=test_module.run, args=(display_window, record_timestamp, enable_buttons))
    current_test_thread.start()

def record_timestamp(event_name):
    timestamp = datetime.now()
    collected_data.append((event_name, timestamp))
    print(f"{event_name}: {timestamp}")

def enable_buttons():
    for button in test_buttons.values():
        button.config(state="normal")
        save_to_csv()
        lsl.save_collected_data()
        time.sleep(1)
        postProcessing.label_data_based_on_events(f'{folder}collected_data.csv', f'{folder}event_data.csv', f'{folder}labeled_data.csv')
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
    filename = os.path.join(csv_folder, "event_data.csv")
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Event", "Timestamp"])
        for data in collected_data:
            writer.writerow(data)
    collected_data.clear()
    print(f"Data saved to {filename}")

def set_window_geometry(window, left_side=True):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    if FULL_SCREEN_MODE:
        window.geometry(f"{screen_width}x{screen_height}+0+0")
    else:
        width = screen_width // 2
        x = 0 if left_side else width
        window.geometry(f"{width}x{screen_height}+{x}+0")

def show_data_and_confirm():
    # Load the data
    data_df = pd.read_csv(f'{csv_folder}/labeled_data.csv')

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





# Start the stream of data
lsl.initialize_streams()
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
    return lambda: run_test(test_name, btn)

# Creating buttons for each test
test_buttons = {}
for test_name in test_names:
    btn = tk.Button(control_window, text=test_name)
    btn.config(command=create_lambda(test_name, btn))
    btn.pack()
    test_buttons[test_name] = btn

control_window.mainloop()
