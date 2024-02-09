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

        # Initialize all required streams
        for stream_type in LSL.streams.keys():
            LSL.__find_and_initialize_stream(stream_type)

    @staticmethod
    def clear_stream_buffers():
        """
        Clears the buffer of each LSL stream to ensure no old data is included in the new collection.
        """
        for stream_type, stream in LSL.streams.items():
            if stream:
                print(f"Clearing buffer for {stream_type} stream...")
                # Continuously pull from the stream until no more samples are returned
                while True:
                    sample, timestamp = stream.pull_sample(timeout=0.0)  # Non-blocking pull
                    if not sample:  # If no sample is returned, the buffer is considered cleared
                        break
                print(f"{stream_type} stream buffer cleared.")

    @staticmethod
    def start_collection():
        """
        Function to start data collection.
        """
        LSL.clear_stream_buffers()
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
        if not event == LSL.collection_label:
            LSL.collection_label = event
            print(f"Labeling Data: {event}")

    @staticmethod
    def stop_label():
        """
        Function to stop labelling each data frame and revert to no label
        """
        if LSL.collection_label:
            print(f"Stopped Labeling Data: {LSL.collection_label}")
            LSL.collection_label = None

    #
    # HELPER METHODS
    #

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
            LSL.streams[stream_type].time_correction()  # Initialize time correction to accurately convert to system
        else:
            print(f"No {stream_type} stream found.")
            exit(1)

    @staticmethod
    def __collect_data():
        """
        Helper function to collect data in the LSL stream on a separate thread to run tests with.

        This works using a constant while loop that continuously polls all LSL streams for samples. If a sample is not
        returned from the poll, it will not be logged. The sample rate is currently as fast as possible with no buffer
        for real-time data processing. Uses StreamInlet.time_correction() to convert LSL to system timestamps using a
        constantly updated offset. The precision of these estimates should be below 1 ms (empirically within +/-0.2 ms).
        """

        while LSL.collecting:
            for stream_type, stream in LSL.streams.items():
                data_row = {'Timestamp': None, 'Label': "Resting" if not LSL.collection_label else LSL.collection_label}

                if stream:
                    sample, timestamp = stream.pull_sample(timeout=0.0)  # Non-blocking pull
                    if sample:
                        # Set timestamp from the first stream and add time correction offset
                        data_row['Timestamp'] = str(datetime.today()) + str(datetime.fromtimestamp(timestamp + stream.time_correction()))

                        # Flatten the data row into a single list and append to collected data
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
                # Formatting breaks everything for some reason:
                # df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%Y-%m-%d %H:%M:%S.%f')
                df = df.sort_values(by='Timestamp')
                df.to_csv(os.path.join(path, f"{stream_type}_data.csv"), index=False)
                print(f"Collected {stream_type} data saved.")
        else:
            print("No data to save.")
