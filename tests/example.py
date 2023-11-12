import random
import tkinter as tk
import lsl
def run(display_window, record_timestamp, enable_buttons_callback):
    lsl.start_collection()
    #lsl_modified.start_collection()
    # Record a start event
    record_timestamp("Blink Start")

    # Create a label for blinking text
    blink_label = tk.Label(display_window, text="Blinking Text", font=("Helvetica", 16))
    blink_label.pack()

    # Function to toggle the visibility of the label
    def toggle_blink():
        if not stop_test_flag:
            blink_label.config(fg="black" if blink_label.cget("fg") == "white" else "white")
            display_window.after(random.randint(1000, 3000), toggle_blink)  # Schedule the next toggle

    # Flag to control stopping of the test
    stop_test_flag = False

    def stop_test():
        nonlocal stop_test_flag
        stop_test_flag = True
        blink_label.destroy()
        lsl.stop_collection()
        record_timestamp("Blink End")
        enable_buttons_callback()
        

    # Start the blinking effect
    toggle_blink()

    # Schedule to stop the test after 15 seconds
    display_window.after(5000, stop_test)
    #lsl_modified.stop_and_save_collection()
