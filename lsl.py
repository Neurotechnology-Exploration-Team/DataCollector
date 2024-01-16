"""
This module contains the LSL class, responsible for handling LSL input, collection, and formatting.
"""
import pylsl
import pandas as pd
import threading
from datetime import datetime

import config


class LSL:
    """
    A class to interface with a local network Laboratory Streaming Layer to collect EEG, accelerometer, and FFT data.
    """

    streams = None
    collected_data = []
    collecting = False
    collection_thread = None

    timestamp_offset = None

    @staticmethod
    def init_lsl_stream():
        """
        MUST BE CALLED TO initialize streams, data, timestamp offset, and the collection thread.
        """
        # Variables to hold streams, data, and the collection thread
        LSL.streams = {'EEG': None, 'Accelerometer': None}  # , 'FFT': None

        # Set up timestamp conversion using a constant offset
        lsl_start_time = datetime.fromtimestamp(pylsl.local_clock())
        system_start_time = datetime.now()
        LSL.timestamp_offset = system_start_time - lsl_start_time

        # Initialize all required streams
        for stream_type in LSL.streams.keys():
            LSL.__find_and_initialize_stream(stream_type)

    @staticmethod
    def start_collection(test_name: str):
        """
        Function to start data collection.
        """
        print("Started data collection.")
        LSL.collecting = True
        LSL.collected_data = []
        LSL.collection_thread = threading.Thread(target=LSL.__collect_data, args=[test_name])
        LSL.collection_thread.start()

    @staticmethod
    def stop_collection():
        """
        Function to stop data collection and save to CSV.
        """
        if LSL.collecting:
            LSL.collecting = False
            LSL.collection_thread.join()
            print("Data collection stopped. Saving collected data.")
            LSL.__save_collected_data(config.COLLECTED_DATA_PATH)

    #
    # HELPER METHODS
    #
    @staticmethod
    def __save_collected_data(path: str):
        """
        Function to save data collected after collection has been stopped. TODO make sure this doesn't overwrite

        :param path: The path to write the collected data to as a CSV file.
        """
        if LSL.collected_data:
            # Define column headers
            eeg_channel_count = LSL.streams['EEG'].info().channel_count() if LSL.streams['EEG'] else 0
            accelerometer_channel_count = LSL.streams['Accelerometer'].info().channel_count() \
                if LSL.streams['Accelerometer'] else 0
            # fft_channel_count = LSL.streams['FFT'].info().channel_count() if LSL.streams['FFT'] else 0

            columns = ['Timestamp'] + \
                      [f'EEG_{i + 1}' for i in range(eeg_channel_count)] + \
                      [f'Accelerometer_{i + 1}' for i in range(accelerometer_channel_count)] + \
                      ['Label']
                    # [f'FFT_{i + 1}' for i in range(fft_channel_count)] + \

            df = pd.DataFrame(LSL.collected_data, columns=columns)
            df['Timestamp'] = pd.to_datetime(df['Timestamp'])
            df = df.sort_values(by='Timestamp')
            df.to_csv(path, index=False)
            print("Collected data saved.")
        else:
            print("No data to save.")

    @staticmethod
    def __lsl_to_system_time(lsl_timestamp):  # TODO idk what type lsl_timestamp is
        """Convert an LSL timestamp to system time."""
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
            exit(1)  # TODO standardize errors + documentation

    @staticmethod
    def __collect_data(test_name: str):
        """
        Helper function to collect data in the LSL stream on a separate thread to run tests with.
        TODO THIS DATA COLLECTION NEEDS TO BE FIXED! CURRENTLY THERE IS NO ACCELEROMETER DATA
        """
        while LSL.collecting:
            data_row = {'Timestamp': None, 'EEG': [], 'Accelerometer': [], 'Label': test_name}  # , 'FFT': []
            for stream_type, stream in LSL.streams.items():
                if stream:
                    sample, timestamp = stream.pull_sample(timeout=0.0)  # Non-blocking pull
                    if sample:
                        if data_row['Timestamp'] is None:
                            data_row['Timestamp'] = LSL.__lsl_to_system_time(timestamp)  # Set timestamp from the first stream
                        data_row[stream_type] = sample
                    else:
                        data_row[stream_type] = [0 for i in range(stream.info().channel_count())]
            if data_row['Timestamp'] is not None:
                # Flatten the data row into a single list
                flattened_data_row = [data_row['Timestamp']] + data_row['EEG'] + data_row['Accelerometer'] + [data_row['Label']]  #  + data_row['FFT']
                LSL.collected_data.append(flattened_data_row)
