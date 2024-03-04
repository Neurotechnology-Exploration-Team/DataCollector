import threading
import time
from tkinter import Label
from queue import Queue
from threading import Thread

timer_label: Label = None
timer_thread: Thread = None
test_start_time: float = None
timer_queue: Queue = Queue()


def init_label(label):
    global timer_label

    timer_label = label
    timer_label.config(text="Elapsed Time: 0.00 seconds")


def update():
    """
    Update the timer label with the elapsed time.
    """
    global timer_queue, timer_label, test_start_time

    if test_start_time is None:
        return

    # TODO Instead message could be initialized above the while loop and the condition could be
    #  while message != "stop". It accomplishes the same thing but makes it a bit more clear as
    #  to when the loop quits - Feedback from Matt L., needs to be tested for thread safety first
    while True:
        # Check for messages in the queue
        try:
            message = timer_queue.get(block=False)
            if message == "stop":
                # Stop the timer
                break
            elif message == "reset":
                # Reset the timer label
                timer_label.config(text="Elapsed Time: 0.00 seconds")
        except:
            pass  # No messages in the queue, continue updating the timer

        # Update the timer label with the elapsed time
        elapsed_time = time.time() - test_start_time
        elapsed_seconds = int(elapsed_time)
        milliseconds = int((elapsed_time - elapsed_seconds) * 100)
        timer_label.config(text=f"Elapsed Time: {elapsed_seconds}.{milliseconds:02d} seconds")
        time.sleep(0.01)  # Update the label every 10 milliseconds


def start():
    global timer_thread, test_start_time
    test_start_time = time.time()  # Record the start time

    # Start the timer
    timer_thread = threading.Thread(target=update)
    timer_thread.start()


def stop():
    """
    Stop the timer.
    """
    global timer_queue

    # Send a "stop" message to the timer thread
    timer_queue.put("stop")


def reset():
    """
    Reset the timer label.
    """
    global timer_queue, timer_label

    # Send a "reset" message to the timer thread
    timer_label.config(text="Elapsed Time: 0.00 seconds")
    timer_queue.put("reset")
