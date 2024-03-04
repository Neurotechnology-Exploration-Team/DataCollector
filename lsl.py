import os.path
from threading import Thread
from pandas import DataFrame
from pylsl import resolve_byprop, StreamInlet

import config

"""
A class to interface with a local network Laboratory Streaming Layer to collect EEG data, responsible for handling
LSL input, collection, and formatting.
"""

streams = {}  # The LSL streams being tracked
collected_data = {}  # The collected data to be held and reviewed between start_collection() and stop_collection()
collecting = False  # Flag if data is currently being collected
collection_thread: Thread = None  # The current thread data is being collected on, if any
collection_label = None  # The current label to be appended to the data, if any


def init_lsl_stream():
    """
    MUST BE CALLED TO initialize streams, data, timestamp offset, and the collection thread.
    """
    global streams, collected_data

    # Variables to hold streams, data, and the collection thread
    for stream_type, enabled in config.SUPPORTED_STREAMS.items():
        if enabled:
            streams[stream_type] = None
            collected_data[stream_type] = []

    # Initialize all required streams
    for stream_type in streams.keys():
        _find_and_initialize_stream(stream_type)


def clear_stream_buffers():
    """
    Clears the buffer of each LSL stream to ensure no old data is included in the new collection.
    """
    global streams

    for stream_type, stream in streams.items():
        if stream:
            print(f"Clearing buffer for {stream_type} stream...")
            # Continuously pull from the stream until no more samples are returned
            while True:
                sample, timestamp = stream.pull_sample(timeout=0.0)  # Non-blocking pull
                if not sample:  # If no sample is returned, the buffer is considered cleared
                    break
            print(f"{stream_type} stream buffer cleared.")


def start_collection():
    """
    Function to start data collection.
    """
    global collecting, collected_data, collection_thread

    clear_stream_buffers()
    print("Started data collection.")
    collecting = True
    for stream_type in collected_data.keys():
        collected_data[stream_type] = []
    collection_thread = Thread(target=_collect_data)
    collection_thread.start()


def stop_collection(path: str):
    """
    Function to stop data collection and save to CSV.

    :param path: Path to the FOLDER that the data should be saved to.
    """
    global collecting, collection_thread

    if collecting:
        collecting = False
        collection_thread.join()
        print("Data collection stopped. Saving collected data.")
        _save_collected_data(path)


def start_label(event: str):
    """
    Function to start labelling each data frame until stop_label() is called
    """
    global collection_label

    if event != collection_label:
        collection_label = event
        print(f"Labeling Data: {event}")


def stop_label():
    """
    Function to stop labelling each data frame and revert to no label
    """
    global collection_label

    if collection_label:
        print(f"Stopped Labeling Data: {collection_label}")
        collection_label = None


def _find_and_initialize_stream(stream_type: str):
    """
    Function to find and initialize a specific LSL stream

    :param stream_type: The type of the LSL stream.
    """
    global streams

    print(f"Looking for a {stream_type} stream...")

    streams_info = resolve_byprop('type', stream_type, 1, config.LSL_RESOLUTION_TIMEOUT)

    if len(streams_info) > 0:
        print(f"{stream_type} stream found.")
        streams[stream_type] = StreamInlet(streams_info[0])
        streams[stream_type].time_correction()  # Initialize time correction to accurately convert to system
    else:
        print(f"No {stream_type} stream found. Exiting Data Collector.")
        exit(1)


def _collect_data():
    """
    Helper function to collect data in the LSL stream on a separate thread to run tests with.

    This works using a constant while loop that continuously polls all LSL streams for samples. If a sample is not
    returned from the poll, it will not be logged. The sample rate is currently as fast as possible with no buffer
    for real-time data processing. Uses StreamInlet.time_correction() to convert LSL to system timestamps using a
    constantly updated offset. The precision of these estimates should be below 1 ms (empirically within +/-0.2 ms).
    """
    global streams, collected_data

    while collecting:
        for stream_type, stream in streams.items():
            data_row = {'Timestamp': None,
                        'Label': config.DEFAULT_LABEL if not collection_label else collection_label}

            if stream:
                sample, timestamp = stream.pull_sample(timeout=0.0)  # Non-blocking pull
                if sample:
                    # Set timestamp from the first stream and add time correction offset
                    data_row['Timestamp'] = timestamp

                    # Flatten the data row into a single list and append to collected data
                    flattened_data_row = [data_row['Timestamp']] + [data_row['Label']] + sample
                    collected_data[stream_type] += [flattened_data_row]


def _save_collected_data(path: str):
    """
    Function to save data collected after collection has been stopped.

    :param path: Path to the FOLDER that the data should be saved to
    """
    global streams, collected_data

    if collected_data:
        for stream_type in streams.keys():
            channel_count = streams[stream_type].info().channel_count() if streams[stream_type] else 0

            # Define column headers
            columns = ['Timestamp'] + ['Label'] + [f'{stream_type}_{i + 1}' for i in range(channel_count)]

            # Convert collected data to a DataFrame, format with columns above, and write to CSV
            df = DataFrame(collected_data[stream_type], columns=columns)
            df = df.sort_values(by='Timestamp')
            df.to_csv(os.path.join(path, f"{stream_type}_data.csv"), index=False)
            print(f"Collected {stream_type} data saved.")
    else:
        print("No data to save.")
