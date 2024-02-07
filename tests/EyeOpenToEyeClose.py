"""
THIS IS AN EXAMPLE OF WHAT A TEST CLASS SHOULD LOOK LIKE. DUPLICATE THIS CLASS AND UPDATE LABELS, ETC TO CREATE A NEW TEST.
"""
import random
import tkinter as tk
import os

from tests.TestGUI import TestGUI
from tests.TestThread import TestThread
import time

import config


class EyeOpenToEyeClose(TestThread):
    """
    The Blink test that extends the TestThread class. Each method should call its super() equivalent to ensure data collection and thread management.
    """

    def __init__(self):
        """
        Initializes and creates the blink label in the display window.
        """
        super().__init__()
        self.image_directory = os.path.join(os.path.dirname(__file__), '..', 'assets', 'EyesOpen.png')
        self.image = tk.PhotoImage(file=self.image_directory)
        self.image2_directory = os.path.join(os.path.dirname(__file__), '..', 'assets', 'EyesClosed.png')
        self.image2 = tk.PhotoImage(file=self.image2_directory)
        # Closed
        self.closed_label = tk.Label(TestGUI.display_window, image=self.image2, borderwidth=0)
        # Opened
        self.open_label = tk.Label(TestGUI.display_window, image=self.image, borderwidth=0)


        self.show_closed = True
        self.show_open = False
        self.next_close = False
        self.next_open = False

        self.interval = random.randint(config.TRANSITION_LOW_INTERVALS, config.TRANSITION_HIGH_INTERVALS)

        self.total_trails = 0



    def run(self):
        """
        Holds the logic to toggle blinking. TestThread will automatically call stop after the duration has ended.
        """
        super().run()
        def toggle():
            # empty function for now
            self.open_label.place_forget()
            self.closed_label.place_forget()
            print ("In the toggle function here are the values")
            print ("Show float", self.show_closed)
            print ("Show Selection", self.show_open)

            if self.total_trails == (config.ITERATIONS_PER_ACTION * 2):
                TestGUI.display_window.after(1, self.stop)

            if self.show_closed:
                print ("Showing the float")
                self.closed_label.place(relx = 0.5, rely = 0.5, anchor='center')
                self.show_closed = False
                self.next_close = False
                self.next_open = True
                TestGUI.display_window.after(self.interval, toggle)  # Schedule the next toggle
                self.total_trails += 1
            elif self.show_open:
                print ("Showing the selection")
                self.open_label.place(relx = 0.5, rely = 0.5, anchor='center')
                self.show_open = False
                self.next_close = True
                self.next_open = False
                TestGUI.display_window.after(self.interval, toggle)
                self.total_trails += 1
            elif self.next_close:
                self.show_closed = True
                self.show_open = False
                TestGUI.display_window.bell()
                TestGUI.display_window.after(1000, toggle)
            elif self.next_open:
                self.show_closed = False
                self.show_open = True
                TestGUI.display_window.bell()
                TestGUI.display_window.after(1000, toggle)


        toggle()

    def stop(self):
        """
        Toggles blinking flag and destroys label.
        """
        self.show_closed = False
        self.show_open = False
        self.next_close = False
        self.next_open = False
        self.interval = 0
        self.total_trails = 0
        self.closed_label.destroy()
        self.open_label.destroy()
        super().stop()
