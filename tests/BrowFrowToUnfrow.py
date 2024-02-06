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


class BrowFrowToUnfrow(TestThread):
    """
    The Blink test that extends the TestThread class. Each method should call its super() equivalent to ensure data collection and thread management.
    In this context closed means unfurrow and open means furrow
    """

    def __init__(self):
        """
        Initializes and creates the blink label in the display window.
        """
        super().__init__()
        self.image_directory = os.path.join(os.path.dirname(__file__), '..', 'assets', 'BrowFurrow.png')
        self.image = tk.PhotoImage(file=self.image_directory)
        self.image2_directory = os.path.join(os.path.dirname(__file__), '..', 'assets', 'BrowUnfurrow.png')
        self.image2 = tk.PhotoImage(file=self.image2_directory)
        # Closed
        self.closed_label = tk.Label(TestGUI.display_window, image=self.image2, borderwidth=0)
        # Opened
        self.open_label = tk.Label(TestGUI.display_window, image=self.image, borderwidth=0)


        self.show_closed = True
        self.show_open = False
        self.next_close = False
        self.next_open = False





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
            if self.show_closed:
                print ("Showing the float")
                self.closed_label.place(relx = 0.5, rely = 0.5, anchor='center')
                self.show_closed = False
                self.next_close = False
                self.next_open = True
                TestGUI.display_window.after(random.randint(config.TEST_LOW_INTERVALS, config.TEST_HIGH_INTERVALS), toggle)  # Schedule the next toggle
            elif self.show_open:
                print ("Showing the selection")
                self.open_label.place(relx = 0.5, rely = 0.5, anchor='center')
                self.show_open = False
                self.next_close = True
                self.next_open = False
                TestGUI.display_window.after(random.randint(config.TEST_LOW_INTERVALS, config.TEST_HIGH_INTERVALS), toggle)
            elif self.next_close:
                self.show_closed = True
                self.show_open = False
                TestGUI.display_window.bell()
                TestGUI.display_window.after(1500, toggle)
            elif self.next_open:
                self.show_closed = False
                self.show_open = True
                TestGUI.display_window.bell()
                TestGUI.display_window.after(1500, toggle)


        toggle()

    def stop(self):
        """
        Toggles blinking flag and destroys label.
        """
        self.show_closed = False
        self.show_open = False
        self.next_close = False
        self.next_open = False
        self.closed_label.destroy()
        self.open_label.destroy()
        super().stop()
