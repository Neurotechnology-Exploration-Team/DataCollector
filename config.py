# LSL configuration
LSL_RESOLUTION_TIMEOUT = 10.0   # Timeout for connecting an LSL stream (seconds)
SUPPORTED_STREAMS = {           # Which streams to enable/data to collect
    'EEG': True,
    'Accelerometer': False,
    'FFT': False
}
DEFAULT_LABEL = "No Event"

# Test length TODO add a simple equation or something to describe test durations
DATA_PADDING_DURATION = 5    # How long to wait before starting and ending a test (default 5 seconds)
BLINK_MIN_INTERVAL = 2.5     # The minimum duration between intervals (default 2.5 seconds)
BLINK_MAX_INTERVAL = 6       # The maximum duration between intervals (default 6 seconds)

ITERATIONS_PER_TEST = 15           # How many iterations run per action (default 30)
ITERATIONS_PER_CONSTANT_TEST = 7  # How many iterations run per constant test (default 5, generally about 5 minutes)

PAUSE_AFTER_TEST = 0.5       # How long to wait after each test iteration (default 0.5 seconds)
TRANSITION_DURATION = 10     # How long to wait before swapping transition states (default 10 seconds)
CONSTANT_TEST_DURATION = 15  # How long a constant test iteration should be (default 20 seconds)
CONSTANT_TEST_BREAK = 5      # How long to break for during constant tests (default 5 seconds)

#
# The main list of all tests corresponding to type and their images.
#
# TODO set up a better list of tests with auditory stimulus config, etc.
TESTS = {
    "Transition": {
        # "Stationary Float to Select": ["Stop.png", "Select.png"],
        # "Stationary Float to Float Left": ["Stop.png", "Left.png"],
        # "Stationary Float to Float Right": ["Stop.png", "Right.png"],
        # "Stationary Float to Float Forward": ["Stop.png", "Up.png"],
        # "Stationary Float to Float Backward": ["Stop.png", "Down.png"],
        # "Eyes Open to Eyes Closed": ["EyesOpen.png", "EyesClosed.png"],
        # "Brow Furrow to Brow Unfurrow": ["BrowFurrow.png", "BrowUnfurrow.png"]
    },
    "Continuous": [
        "Stationary float to float movement",
        "Float movement"
    ],
    "Constant": {  # Images currently not used, only text is used
        # "Eyes Open": "EyesOpen.png",
        # "Eyes Closed": "EyesClosed.png",
        "Brow Furrow": "BrowFurrow.png",
        "Brow Unfurrow": "BrowUnfurrow.png",
        # "Stationary Floating": "Stop.png",
        # "Float Left": "Left.png",
        # "Float Right": "Right.png",
        # "Float Forward": "Up.png",
        # "Float Backward": "Down.png",
        # "Select": "Select.png"
    },
    "Blink": [  # No images for blinking tests
        "Blink"
    ]
}

# Save path configuration (<DATA_PATH>/PXXX/SXXX/trial_XX/<STREAM_TYPE>_data.csv)
SAVED_DATA_PATH = "csv_downloads"
