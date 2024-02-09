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
TEST_MIN_INTERVAL = 2500       # The minimum duration between intervals
TEST_MAX_INTERVAL = 6000       # The maximum duration between intervals
ITERATIONS_PER_ACTION = 2      # How many iterations run per action (default 20, change for testing)
ITERATION_DURATION = 1 * 1000  # How many milliseconds a test iteration appears for

# Subject information
NUMBER_OF_SUBJECTS = 10

# Save path configuration (<DATA_PATH>/PXXX/SXXX/trial_XX/<STREAM_TYPE>_data.csv)
DATA_PATH = "csv_downloads"
