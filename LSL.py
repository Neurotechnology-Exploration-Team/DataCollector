import pylsl
import pandas as pd
import threading
from datetime import datetime

LSL_RESOLUTION_TIMEOUT = 10.0  # Timeout (in seconds) for an LSL stream


class LSL:
    """
    A class to interface with a local network Laboratory Streaming Layer to collect EEG, accelerometer, and FFT data.

    Authors: Alex Burbano, Ian Dunn
    """

    def __init__(self):
        """
        The main constructor to initialize streams, data, timestamp offset, and the collection thread.
        """
        # Variables to hold streams, data, and the collection thread
        self.streams = {'EEG': None, 'Accelerometer': None, 'FFT': None}
        self.collected_data = []
        self.collecting = False
        self.collection_thread = None

        # Set up timestamp conversion using a constant offset
        lsl_start_time = datetime.fromtimestamp(pylsl.local_clock())
        system_start_time = datetime.now()
        self.TIMESTAMP_OFFSET = system_start_time - lsl_start_time

        # Initialize all required streams
        for stream_type in self.streams.keys():
            self.__find_and_initialize_stream(stream_type)

    def start_collection(self):
        """
        Function to start data collection.
        """
        print("Started data collection.")
        self.collecting = True
        self.collected_data = []
        self.collection_thread = threading.Thread(target=self.__collect_data)
        self.collection_thread.start()

    def stop_collection(self, saved_data_path: str):
        """
        Function to stop data collection and save to CSV.

        :param saved_data_path: The path to save the data to.
        """
        if self.collecting:
            self.collecting = False
            self.collection_thread.join()
            print("Data collection stopped. Saving collected data.")
            self.__save_collected_data(saved_data_path)

    #
    # HELPER METHODS
    #
    def __save_collected_data(self, path):
        """
        Function to save data collected after collection has been stopped.
        """
        if self.collected_data:
            # Define column headers
            eeg_channel_count = self.streams['EEG'].info().channel_count() if self.streams['EEG'] else 0
            accelerometer_channel_count = self.streams['Accelerometer'].info().channel_count() if self.streams[
                'Accelerometer'] else 0
            fft_channel_count = self.streams['FFT'].info().channel_count() if self.streams['FFT'] else 0

            columns = ['Timestamp'] + \
                      [f'EEG_{i + 1}' for i in range(eeg_channel_count)] + \
                      [f'Accelerometer_{i + 1}' for i in range(accelerometer_channel_count)] + \
                      [f'FFT_{i + 1}' for i in range(fft_channel_count)]

            df = pd.DataFrame(self.collected_data, columns=columns)
            df['Timestamp'] = pd.to_datetime(df['Timestamp'])
            df = df.sort_values(by='Timestamp')
            df.to_csv(path, index=False)
            print("Collected data saved.")
        else:
            print("No data to save.")

    def __lsl_to_system_time(self, lsl_timestamp):
        """Convert an LSL timestamp to system time."""
        return datetime.fromtimestamp(lsl_timestamp + self.TIMESTAMP_OFFSET.total_seconds())

    def __find_and_initialize_stream(self, stream_type: str):
        """
        Function to find and initialize a specific LSL stream

        :param stream_type: The type of the LSL stream.
        """
        print(f"Looking for a {stream_type} stream...")

        streams_info = pylsl.resolve_byprop('type', stream_type, 1, LSL_RESOLUTION_TIMEOUT)

        if len(streams_info) > 0:
            print(f"{stream_type} stream found.")
            self.streams[stream_type] = pylsl.StreamInlet(streams_info[0])
        else:
            print(f"No {stream_type} stream found.")
            exit(1)  # TODO standardize errors + documentation

    def __collect_data(self):
        while self.collecting:
            data_row = {'Timestamp': None, 'EEG': [], 'Accelerometer': [], 'FFT': []}
            for stream_type, stream in self.streams.items():
                if stream:
                    sample, timestamp = stream.pull_sample(timeout=0.0)  # Non-blocking pull
                    if sample:
                        system_timestamp = self.__lsl_to_system_time(timestamp)
                        if data_row['Timestamp'] is None:
                            data_row['Timestamp'] = system_timestamp  # Set timestamp from the first stream
                        data_row[stream_type] = sample
            if data_row['Timestamp'] is not None:
                # Flatten the data row into a single list
                flattened_data_row = [data_row['Timestamp']] + data_row['EEG'] + data_row['Accelerometer'] + data_row[
                    'FFT']
                self.collected_data.append(flattened_data_row)
