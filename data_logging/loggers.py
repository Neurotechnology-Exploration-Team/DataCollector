import csv
from datetime import datetime
import pandas as pd

import config


class CollectedDataLogger:
    @staticmethod
    def record_data(collected_data, eeg_channel_count, accelerometer_channel_count, fft_channel_count):
        """
        Function to save data collected after collection has been stopped.

        :param path: The path to write the collected data to as a CSV file.
        """
        if collected_data:
            columns = ['Timestamp'] + \
                      [f'EEG_{i + 1}' for i in range(eeg_channel_count)] + \
                      [f'Accelerometer_{i + 1}' for i in range(accelerometer_channel_count)] + \
                      [f'FFT_{i + 1}' for i in range(fft_channel_count)]

            df = pd.DataFrame(collected_data, columns=columns)
            df['Timestamp'] = pd.to_datetime(df['Timestamp'])
            df = df.sort_values(by='Timestamp')
            df.to_csv(config.COLLECTED_DATA_PATH, index=False)
            print(f"LSL Data saved to {config.COLLECTED_DATA_PATH}")
        else:
            print("No data to save.")


class EventLogger:
    """
    A static class to log test events in a separate CSV
    """
    event_data = []

    @staticmethod
    def record_timestamp(event_name):
        """
        Record the time the data was collected along with the event

        :param event_name: Event that was collected
        """
        timestamp = datetime.now()
        EventLogger.event_data.append((event_name, timestamp))
        print(f"{event_name}: {timestamp}")

    @staticmethod
    def save_to_csv() -> bool:
        """
        Write all data to the csv files

        :return: If the writing was successful
        """
        if not EventLogger.event_data:
            return False

        # Wrap it to catch any file issues
        try:
            with open(config.EVENT_DATA_PATH, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Event", "Timestamp"])
                for data in EventLogger.event_data:
                    writer.writerow(data)
        except Exception:
            return False

        EventLogger.event_data.clear()
        print(f"Event Data saved to {config.EVENT_DATA_PATH}")

        return True

    @staticmethod
    def clear_data():
        EventLogger.event_data.clear()
