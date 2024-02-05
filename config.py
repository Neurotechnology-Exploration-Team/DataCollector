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
DATA_PADDING_DURATION = 1.0    # How many seconds to wait before starting and ending a test
TEST_DURATION = 5 * 1000       # How many milliseconds the test should take. Default to 30 for trials
MIN_BLINK_DURATION = 1 * 1000  # How many milliseconds the minimum duration of a blinking action label should be
MAX_BLINK_DURATION = 3 * 1000  # How many milliseconds the maximum duration of a blinking action label should be

# Subject information
NUMBER_OF_SUBJECTS = 10

# Save path configuration (<DATA_PATH>/PXXX/SXXX/trial_XX/<STREAM_TYPE>_data.csv)
DATA_PATH = "csv_downloads"
