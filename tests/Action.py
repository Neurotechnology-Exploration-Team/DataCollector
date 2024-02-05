import random
import tkinter as tk
import os

import config
from tests.TestGUI import TestGUI
from tests.TestThread import TestThread


class Action(TestThread):
    """
    The Action test that extends the TestThread class. Each method should call its super() equivalent to ensure data
    collection and thread management.
    """

    def __init__(self, action_name):
        """
        Initializes and creates the Action label in the display window.

<<<<<<< HEAD
        self.action_label = tk.Label(TestGUI.display_window, text=self.label, font=("Helvetica", 16))
        self.action_label.pack()

        self.action = True
        self.name = actionName
=======
        :param action_name: The name of the action.
        """
        super().__init__(action_name)

        # Setup blinking label
        self.action_label = tk.Label(TestGUI.display_window, text=self.name, font=("Helvetica", 16))
        self.action_label.pack()
        self.action_enabled = True  # Flag for when to stop blinking action label
>>>>>>> 08c7aaed21cf9ff253ba610f248f62b8c51a0e72

    def run(self):
        """
        Holds the logic to toggle blinking. TestThread will automatically call stop after the duration has ended.
        """

        '''
        test_directory = 'tests'
        test_names = [filename.split('.')[0]
                      for filename in os.listdir(test_directory)
                      if filename.endswith('.py') and not filename.startswith('Test') and not filename.startswith('__init__')]
        '''

        picture_directory = 'assets'
        picture_names = [filename.split('.')[0]
                         for filename in os.listdir(picture_directory)]

        print (picture_names)

        if (self.name.split(' ')[-1] in picture_names):
            print ("We will be displaying picture")
            print (self.name.split)


        super().run()

        def toggle_action():
            """
            Function to toggle blinking action label with random intervals.
            """
            if self.action_enabled:
                self.action_label.config(fg="black" if self.action_label.cget("fg") == "white" else "white")
<<<<<<< HEAD
                TestGUI.display_window.after(random.randint(1000, 3000), toggle_action)  # Schedule the next toggle
=======
                # Schedule the next toggle
                TestGUI.display_window.after(
                    random.randint(config.MIN_BLINK_DURATION, config.MAX_BLINK_DURATION),
                    toggle_action)
>>>>>>> 08c7aaed21cf9ff253ba610f248f62b8c51a0e72

        # Start the blinking effect
        toggle_action()

    def stop(self):
        """
        Toggles blinking flag and destroys label.
        """
        self.action_enabled = False
        self.action_label.destroy()

        super().stop()
