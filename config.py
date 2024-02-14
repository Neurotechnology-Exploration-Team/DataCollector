# Graph confirmation configuration
WIDTH_PER_GRAPH = 400
HEIGHT_PER_GRAPH = 80

# LSL configuration
LSL_RESOLUTION_TIMEOUT = 10.0   # Timeout (in seconds) for an LSL stream
SUPPORTED_STREAMS = {           # Which streams to enable
    'EEG': True,
    'Accelerometer': False,
    'FFT': False
}

# Test length
DATA_PADDING_DURATION = 5.0    # How many seconds to wait before starting and ending a test
BLINK_MIN_INTERVAL = 2500       # The minimum duration between intervals
BLINK_MAX_INTERVAL = 6000       # The maximum duration between intervals
ITERATIONS_PER_ACTION = 5       # How many iterations run per action (default 30, change for testing)

TESTS = {
    "Transition": {
        "Stationary Float to Select": ["Stop.png", "Select.png"],  # TODO right image?
        "Stationary Float to Float Left": ["Stop.png", "Left.png"],  # TODO right image?
        "Stationary Float to Float Right": ["Stop.png", "Right.png"],  # TODO right image?
        "Stationary Float to Float Up": ["Stop.png", "Up.png"],  # TODO right image?
        "Stationary Float to Float Down": ["Stop.png", "Down.png"],  # TODO right image?
        "Eyes Open and Close": ["EyesOpen.png", "EyesClosed.png"],
        "Brow Furrow and Unfurrow": ["BrowFurrow.png", "BrowUnfurrow.png"]
    },
    "Constant": {  # Currently not used, only text is used
        "Eyes Open": "EyesOpen.png",
        "Eyes Closed": "EyesClosed.png",
        "Brow Furrow": "BrowFurrow.png",
        "Brow Unfurrow": "BrowUnfurrow.png",
        "Stationary Floating": "Stop.png",  # TODO right image?
        "Float Left": "Left.png",
        "Float Right": "Right.png",
        "Float Up": "Up.png",
        "Float Down": "Down.png",
        "Select": "Stop.png"  # TODO right image?
    },
    "Blink": [
        "Blink"
    ]
}

# Subject information
NUMBER_OF_SUBJECTS = 10

# Save path configuration (<DATA_PATH>/PXXX/SXXX/trial_XX/<STREAM_TYPE>_data.csv)
DATA_PATH = "csv_downloads"
