import tkinter as tk

import config
from LSL import LSL
from tests.TestGUI import TestGUI
from tests.TestThread import TestThread


class TransitionTest(TestThread):
    """

    """

    def __init__(self, name, image_directory_1, image_directory_2):
        """
        Initializes and creates the transition labels in the display window.
        """
        super().__init__(name)

        self.image_1 = tk.PhotoImage(file=image_directory_1)
        self.image_2 = tk.PhotoImage(file=image_directory_2)

        split = " to " if " to " in name else " and "
        self.label_1 = name.split(split)[0]
        self.label_2 = name.split(split)[1]

        self.firstImage = True
        self.current_label = None

    def run_test(self):
        """
        Main loop that runs and schedules the next iteration of the test
        """
        if self.iteration == config.ITERATIONS_PER_ACTION:
            self.running = False

        if self.running:
            if self.firstImage:
                LSL.start_label(self.label_1)
                self.current_label = tk.Label(TestGUI.display_window, image=self.image_1, borderwidth=0)
            else:
                LSL.start_label(self.label_2)
                self.current_label = tk.Label(TestGUI.display_window, image=self.image_2, borderwidth=0)

            self.playsound()
            self.current_label.place(relx=0.5, rely=0.5, anchor='center')

            def swap():
                self.firstImage = not self.firstImage
                self.current_label.destroy()
                self.run_test()

            self.test_job_id = TestGUI.display_window.after(10000, swap)  # TODO how long per transition state + config

            self.iteration += 1
        else:
            # Stop test thread
            self.running = False
            self.current_label.destroy()

            LSL.stop_label()
            self.stop()
