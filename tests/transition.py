import tkinter as tk

import config
from lsl import LSL
from tests.thread import TestThread


class TransitionTest(TestThread):
    """
    The Transition test that extends the TestThread class. Uses images and beeps to swap from one state to another.

    Visual (images) and auditory stimulus
    """

    def __init__(self, controller, name, image_path_1, image_path_2):
        """
        Initializes and creates the transition labels in the display window.

        :param name: The name of the test. Should be "<state 1> to <state 2>" for correct labeling.
        :param image_path_1: The path to the image of state 1
        :param image_path_2: The path to the image of state 2
        """
        super().__init__(controller, name)

        self.image_1 = tk.PhotoImage(file=image_path_1)
        self.image_2 = tk.PhotoImage(file=image_path_2)

        # Derive labels from each half of the test name
        self.label_1 = name.split(" to ")[0]
        self.label_2 = name.split(" to ")[1]

        self.firstImage = True
        self.current_image = None

    def run_test(self):
        """
        Main loop that runs and schedules the next iteration of the test
        """
        if self.iteration == config.ITERATIONS_PER_TEST:
            self.running = False

        if self.running:
            # Display current image and start labeling based on flag
            if self.firstImage:
                LSL.start_label(self.label_1)
                self.current_image = self.controller.gui.place_image(self.image_1)
            else:
                LSL.start_label(self.label_2)
                self.current_image = self.controller.gui.place_image(self.image_2)

            self.playsound()  # Auditory stimulus

            def swap():
                """
                Function to swap the images for transition states.
                """
                self.firstImage = not self.firstImage
                self.run_test()

            self.controller.start_delay(config.TRANSITION_DURATION * 1000, swap)

            self.iteration += 1
        else:
            # Stop test thread
            self.running = False
            self.controller.gui.destroy_current_element()

            LSL.stop_label()
            self.stop()
