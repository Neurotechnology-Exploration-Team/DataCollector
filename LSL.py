"""
This module contains the LSL class, responsible for handling LSL input, collection, and formatting.
"""
import os.path
import threading
from datetime import datetime
import pandas as pd
import pylsl

import config


class LSL:
    """
    A class to interface with a local network Laboratory Streaming Layer to collect EEG and Accelerometer data.
    """

    streams = None  # The LSL streams being tracked
    collected_data = None  # The collected data to be held and reviewed between start_collection() and stop_collection()
    collecting = False  # Flag if data is currently being collected
    collection_thread = None  # The current thread data is being collected on, if any
    collection_label = None  # The current label to be appended to the data, if any

    timestamp_offset = None  # The offset between LSL and system timestamps. TODO is this still necessary

    @staticmethod
    def init_lsl_stream():
        """
        MUST BE CALLED TO initialize streams, data, timestamp offset, and the collection thread.
        """
        # Variables to hold streams, data, and the collection thread
        LSL.streams = {}
        LSL.collected_data = {}
        for stream_type, enabled in config.SUPPORTED_STREAMS.items():
            if enabled:
                LSL.streams[stream_type] = None
                LSL.collected_data[stream_type] = []

        # Set up timestamp conversion using a constant offset
        lsl_start_time = datetime.fromtimestamp(pylsl.local_clock())
        system_start_time = datetime.now()
        LSL.timestamp_offset = system_start_time - lsl_start_time

        # Initialize all required streams
        for stream_type in LSL.streams.keys():
            LSL.__find_and_initialize_stream(stream_type)

    @staticmethod
    def start_collection():
        """
        Function to start data collection.
        """
        print("Started data collection.")
        LSL.collecting = True
        for stream_type in LSL.collected_data.keys():
            LSL.collected_data[stream_type] = []
        LSL.collection_thread = threading.Thread(target=LSL.__collect_data)
        LSL.collection_thread.start()

    @staticmethod
    def stop_collection(path: str):
        """
        Function to stop data collection and save to CSV.

        :param path: Path to the FOLDER that the data should be saved to.
        """
        if LSL.collecting:
            LSL.collecting = False
            LSL.collection_thread.join()
            print("Data collection stopped. Saving collected data.")
            LSL.__save_collected_data(path)

    @staticmethod
    def start_label(event: str):
        """
        Function to start labelling each data frame until stop_label() is called
        """
        LSL.collection_label = event
        print(f"Labeling Data: {event}")

    @staticmethod
    def stop_label():
        """
        Function to stop labelling each data frame and revert to no label
        """
        print(f"Stopped Labeling Data: {LSL.collection_label}")
        LSL.collection_label = None

    #
    # HELPER METHODS
    #

    @staticmethod
    def __lsl_to_system_time(lsl_timestamp):  # TODO idk what type lsl_timestamp is
        """
        Converts an LSL timestamp to system time.
        """
        return datetime.fromtimestamp(lsl_timestamp + LSL.timestamp_offset.total_seconds())

    @staticmethod
    def __find_and_initialize_stream(stream_type: str):
        """
        Function to find and initialize a specific LSL stream

        :param stream_type: The type of the LSL stream.
        """
        print(f"Looking for a {stream_type} stream...")

        streams_info = pylsl.resolve_byprop('type', stream_type, 1, config.LSL_RESOLUTION_TIMEOUT)

        if len(streams_info) > 0:
            print(f"{stream_type} stream found.")
            LSL.streams[stream_type] = pylsl.StreamInlet(streams_info[0])
        else:
            print(f"No {stream_type} stream found.")
            exit(1)

    @staticmethod
    def __collect_data():
        """
        Helper function to collect data in the LSL stream on a separate thread to run tests with.
        """

        while LSL.collecting:
            for stream_type, stream in LSL.streams.items():
                data_row = {'Timestamp': None, 'Label': "" if not LSL.collection_label else LSL.collection_label}

                if stream:
                    # TODO adjust sample rate
                    sample, timestamp = stream.pull_sample(timeout=0.0)  # Non-blocking pull
                    if sample:
                        if data_row['Timestamp'] is None:
                            # Set timestamp from the first stream
                            data_row['Timestamp'] = LSL.__lsl_to_system_time(timestamp)

                        # Flatten the data row into a single list
                        flattened_data_row = [data_row['Timestamp']] + [data_row['Label']] + sample
                        LSL.collected_data[stream_type] += [flattened_data_row]

    @staticmethod
    def __save_collected_data(path: str):
        """
        Function to save data collected after collection has been stopped.

        :param path: Path to the FOLDER that the data should be saved to
        """

        if LSL.collected_data:
            for stream_type in LSL.streams.keys():
                channel_count = LSL.streams[stream_type].info().channel_count() if LSL.streams[stream_type] else 0

                # Define column headers
                columns = ['Timestamp'] + ['Label'] + [f'{stream_type}_{i + 1}' for i in range(channel_count)]

                # Convert collected data to a DataFrame, format with columns above, and write to CSV
                df = pd.DataFrame(LSL.collected_data[stream_type], columns=columns)
                df['Timestamp'] = pd.to_datetime(df['Timestamp'])
                df = df.sort_values(by='Timestamp')
                df.to_csv(os.path.join(path, f"{stream_type}_data.csv"), index=False)
                print(f"Collected {stream_type} data saved.")
        else:
            print("No data to save.")
