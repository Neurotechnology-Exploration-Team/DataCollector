import threading
import time
from queue import Queue


class Timer:
    def __init__(self, timer_label):
        self.timer_label = timer_label
        self.timer_queue = Queue()  # Initialize a queue for communication between thread
        self.test_start_time = None
        self.timer_thread = None

    def _update_timer(self):
        """
        Update the timer label with the elapsed time.
        """
        # TODO Instead message could be initialized above the while loop and the condition could be
        #  while message != "stop". It accomplishes the same thing but makes it a bit more clear as
        #  to when the loop quits - Feedback from Matt L., needs to be tested for thread safety first
        while True:
            # Check for messages in the queue
            try:
                message = self.timer_queue.get(block=False)
                if message == "stop":
                    # Stop the timer
                    break
                elif message == "reset":
                    # Reset the timer label
                    self.timer_label.config(text="Elapsed Time: 0.00 seconds")
            except:
                pass  # No messages in the queue, continue updating the timer

            # Update the timer label with the elapsed time
            elapsed_time = time.time() - self.test_start_time
            elapsed_seconds = int(elapsed_time)
            milliseconds = int((elapsed_time - elapsed_seconds) * 100)
            self.timer_label.config(text=f"Elapsed Time: {elapsed_seconds}.{milliseconds:02d} seconds")
            time.sleep(0.01)  # Update the label every 10 milliseconds

    def start_timer(self):
        # Initialize test start time
        self.test_start_time = time.time()  # Record the start time

        # Start the timer
        self.timer_thread = threading.Thread(target=self._update_timer)
        self.timer_thread.start()

    def stop_timer(self):
        """
        Stop the timer.
        """
        # Send a "stop" message to the timer thread
        self.timer_queue.put("stop")

    def reset_timer(self):
        """
        Reset the timer label.
        """
        # Send a "reset" message to the timer thread
        self.timer_label.config(text="Elapsed Time: 0.00 seconds")
        self.timer_queue.put("reset")
