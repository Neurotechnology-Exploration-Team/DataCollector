import pylsl
import pandas as pd
import threading
from datetime import datetime


# Global variables to hold streams, data, and the collection thread
streams = {'EEG': None, 'Accelerometer': None, 'FFT': None}
collected_data = []
collecting = False
collection_thread = None

lsl_start_time = None
system_start_time = None

def initialize_time_sync():
    global lsl_start_time, system_start_time
    lsl_start_time = pylsl.local_clock()
    system_start_time = datetime.now()

def lsl_to_system_time(lsl_timestamp):
    """Convert an LSL timestamp to system time."""
    global lsl_start_time, system_start_time
    offset = system_start_time - datetime.fromtimestamp(lsl_start_time)
    return datetime.fromtimestamp(lsl_timestamp + offset.total_seconds())

# Function to find and initialize a specific LSL stream
def find_and_initialize_stream(stream_type):
    print(f"Looking for a {stream_type} stream...")
    streams_info = pylsl.resolve_stream('type', stream_type)
    if streams_info:
        print(f"{stream_type} stream found.")
        streams[stream_type] = pylsl.StreamInlet(streams_info[0])
    else:
        print(f"No {stream_type} stream found.")

# Function to initialize all required streams
def initialize_streams():
    global lsl_start_time, system_start_time
    lsl_start_time = pylsl.local_clock()
    system_start_time = datetime.now()
    for stream_type in streams.keys():
        find_and_initialize_stream(stream_type)

def collect_data():
    global collected_data, collecting
    while collecting:
        data_row = {'Timestamp': None, 'EEG': [], 'Accelerometer': [], 'FFT': []}
        for stream_type, stream in streams.items():
            if stream:
                sample, timestamp = stream.pull_sample(timeout=0.0)  # Non-blocking pull
                if sample:
                    system_timestamp = lsl_to_system_time(timestamp)
                    if data_row['Timestamp'] is None:
                        data_row['Timestamp'] = system_timestamp  # Set timestamp from the first stream
                    data_row[stream_type] = sample
        if data_row['Timestamp'] is not None:
            # Flatten the data row into a single list
            flattened_data_row = [data_row['Timestamp']] + data_row['EEG'] + data_row['Accelerometer'] + data_row['FFT']
            collected_data.append(flattened_data_row)
def save_collected_data():
    global collected_data
    if collected_data:
        # Define column headers
        eeg_channel_count = streams['EEG'].info().channel_count() if streams['EEG'] else 0
        accelerometer_channel_count = streams['Accelerometer'].info().channel_count() if streams['Accelerometer'] else 0
        fft_channel_count = streams['FFT'].info().channel_count() if streams['FFT'] else 0

        columns = ['Timestamp'] + \
                  [f'EEG_{i+1}' for i in range(eeg_channel_count)] + \
                  [f'Accelerometer_{i+1}' for i in range(accelerometer_channel_count)] + \
                  [f'FFT_{i+1}' for i in range(fft_channel_count)]

        df = pd.DataFrame(collected_data, columns=columns)
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        df = df.sort_values(by='Timestamp')
        df.to_csv('csv_downloads/collected_data.csv', index=False)
        print("Collected data saved.")
    else:
        print("No data to save.")




# Function to start data collection
def start_collection():
    global collecting, collection_thread
    print("Started data collection.")
    collecting = True
    collected_data = []
    collection_thread = threading.Thread(target=collect_data)
    collection_thread.start()

# Function to stop data collection
def stop_collection():
    global collecting, collection_thread
    if collecting:
        collecting = False
        collection_thread.join()
        print("Data collection stopped.")

