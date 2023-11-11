import random
import tkinter as tk

def run(display_window, record_timestamp, enable_buttons_callback):
    # Record a start event
    record_timestamp("Test Start")

    # Create a label for blinking text
    blink_label = tk.Label(display_window, text="Blinking Text", font=("Helvetica", 16))
    blink_label.pack()

    # Function to toggle the visibility of the label
    def toggle_blink():
        if not stop_test_flag:
            blink_label.config(fg="black" if blink_label.cget("fg") == "white" else "white")
            record_timestamp("Blink Toggled")
            display_window.after(random.randint(1000, 3000), toggle_blink)  # Schedule the next toggle

    # Flag to control stopping of the test
    stop_test_flag = False

    def stop_test():
        nonlocal stop_test_flag
        stop_test_flag = True
        blink_label.destroy()
        record_timestamp("Test End")
        enable_buttons_callback()

    # Start the blinking effect
    toggle_blink()

    # Schedule to stop the test after 15 seconds
    display_window.after(15000, stop_test)
