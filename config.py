FULL_SCREEN_MODE = False  # Whether to run the test in one or two windows (?)

# Graph confirmation configuration
WIDTH_PER_GRAPH = 400
HEIGHT_PER_GRAPH = 80

# LSL configuration
LSL_RESOLUTION_TIMEOUT = 10.0  # Timeout (in seconds) for an LSL stream
DISCARD_ZERO_VALUES = False
SUPPORTED_STREAMS = {'EEG': True,
                     'Accelerometer': False,
                     'FFT': False}

# Test length
DATA_PADDING_DURATION = 1.0  # How many seconds to wait before starting and ending a test
TEST_DURATION = 5 * 1000  # How many milliseconds the test should take. Default to 30 for trials

# Subject information
NUMBER_OF_SUBJECTS = 10

# Save path configuration (DATA_PATH/<id>/<test>/trial_<trial_number>/FILENAME)
DATA_PATH = "csv_downloads"
