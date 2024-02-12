import os
from pygame import mixer
from LSL import LSL
from tests.TestThread import TestThread


class BlinkTest(TestThread):
    """
    The Blink test that extends the TestThread class.

    Audio only
    TODO Test
    """

    def __init__(self, name):
        """
        Initializes the image assets for the display window.
        """
        super().__init__(name)

    def start_iteration(self):
        """
        Creates and displays a new label for each iteration.
        """
        super().start_iteration()

        self.playsound()

        LSL.start_label(self.name)

    def stop_iteration(self):
        """
        Destroys the label after each iteration.
        """
        super().stop_iteration()

        LSL.stop_label()
