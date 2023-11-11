import pylsl
import pandas as pd
import numpy as np
import time

# Function to find a specific LSL stream
def find_stream(stream_type):
    print(f"Looking for a {stream_type} stream...")
    streams = pylsl.resolve_stream('type', stream_type)
    if streams:
        print(f"{stream_type} stream found.")
        return streams[0]
    else:
        print(f"No {stream_type} stream found.")
        return None

# Connect to EEG, Accelerometer, and FFT streams
eeg_stream_info = find_stream('EEG')
accel_stream_info = find_stream('Accelerometer')
fft_stream_info = find_stream('FFT')

# Create StreamInlets
eeg_inlet = pylsl.StreamInlet(eeg_stream_info) if eeg_stream_info else None
accel_inlet = pylsl.StreamInlet(accel_stream_info) if accel_stream_info else None
fft_inlet = pylsl.StreamInlet(fft_stream_info) if fft_stream_info else None

# Data collection
data = []
start_time = time.time()
collection_duration = 30  # Collect data for 30 seconds

while time.time() - start_time < collection_duration:
    eeg_data, eeg_timestamp = eeg_inlet.pull_sample() if eeg_inlet else ([], None)
    accel_data, accel_timestamp = accel_inlet.pull_sample() if accel_inlet else ([], None)
    fft_data, fft_timestamp = fft_inlet.pull_sample() if fft_inlet else ([], None)

    # Create a single record for the current timestamp
    record = [eeg_timestamp or accel_timestamp or fft_timestamp]
    record.extend(eeg_data if eeg_data else [np.nan] * eeg_inlet.info().channel_count())
    record.extend(accel_data if accel_data else [np.nan] * accel_inlet.info().channel_count())
    record.extend(fft_data if fft_data else [np.nan] * fft_inlet.info().channel_count())
    
    data.append(record)

# Convert to DataFrame
columns = ['Timestamp'] + [f'EEG_{i}' for i in range(eeg_inlet.info().channel_count())] + \
           [f'Accel_{i}' for i in range(accel_inlet.info().channel_count())] + \
           [f'FFT_{i}' for i in range(fft_inlet.info().channel_count())]

df = pd.DataFrame(data, columns=columns)

# Save to CSV
df.to_csv('collected_data.csv', index=False)

print("Data collection complete. Data saved to 'collected_data.csv'")
