"""
THIS IS AN EXAMPLE OF WHAT A TEST CLASS SHOULD LOOK LIKE. DUPLICATE THIS CLASS AND UPDATE LABELS, ETC TO CREATE A NEW TEST.
"""
import random
import tkinter as tk
import os

from tests.TestGUI import TestGUI
from tests.TestThread import TestThread
import time


class BrowFrowToUnfrow(TestThread):
    """
    The Blink test that extends the TestThread class. Each method should call its super() equivalent to ensure data collection and thread management.
    """

    def __init__(self):
        """
        Initializes and creates the blink label in the display window.
        """
        super().__init__()
        self.image_directory = os.path.join(os.path.dirname(__file__), '..', 'assets', 'right.PNG')
        self.image = tk.PhotoImage(file=self.image_directory)
        self.float_label = tk.Label(TestGUI.display_window, text="Brow Unfrowed", font=("Helvetica", 16), background='black')
        self.image_label = tk.Label(TestGUI.display_window, text="Brow Frowed", font=("Helvetica", 16), background='black')

        self.show_float = True
        self.show_selection = False
        self.next_float = False
        self.next_selection = False





    def run(self):
        """
        Holds the logic to toggle blinking. TestThread will automatically call stop after the duration has ended.
        """
        super().run()
        def toggle():
            # empty function for now
            self.image_label.place_forget()
            self.float_label.place_forget()
            print ("In the toggle function here are the values")
            print ("Show float", self.show_float)
            print ("Show Selection", self.show_selection)
            if self.show_float:
                print ("Showing the float")
                self.float_label.place(relx = 0.5, rely = 0.5, anchor='center')
                self.show_float = False
                self.next_float = False
                self.next_selection = True
                TestGUI.display_window.after(3000, toggle)  # Schedule the next toggle
            elif self.show_selection:
                print ("Showing the selection")
                self.image_label.place(relx = 0.5, rely = 0.5, anchor='center')
                self.show_selection = False
                self.next_float = True
                self.next_selection = False
                TestGUI.display_window.after(3000, toggle)
            elif self.next_float:
                self.show_float = True
                self.show_selection = False
                TestGUI.display_window.bell()
                TestGUI.display_window.after(1500, toggle)
            elif self.next_selection:
                self.show_float = False
                self.show_selection = True
                TestGUI.display_window.bell()
                TestGUI.display_window.after(1500, toggle)


        toggle()

    def stop(self):
        """
        Toggles blinking flag and destroys label.
        """
        self.show_float = False
        self.show_selection = False
        self.next_float = False
        self.next_selection = False
        self.float_label.destroy()
        self.image_label.destroy()
        super().stop()
