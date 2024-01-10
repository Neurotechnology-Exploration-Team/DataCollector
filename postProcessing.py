import pandas as pd


def label_data_based_on_events(data_csv, events_csv, output_csv):
    # Load the data and the events
    data_df = pd.read_csv(data_csv)
    events_df = pd.read_csv(events_csv)

    # Convert timestamps to datetime
    data_df['Timestamp'] = pd.to_datetime(data_df['Timestamp'])
    events_df['Timestamp'] = pd.to_datetime(events_df['Timestamp'])

    # Initialize a new column for labels
    data_df['Label'] = ''

    # Loop through each event and label the data
    for i in range(len(events_df) - 1):
        start_event = events_df.iloc[i]
        end_event = events_df.iloc[i + 1]

        # Check for specific event labels if needed, e.g., "Blink Start" and "Blink End"
        if start_event['Event'] == 'Blink Start' and end_event['Event'] == 'Blink End':
            # Label data between these timestamps
            mask = (data_df['Timestamp'] >= start_event['Timestamp']) & (data_df['Timestamp'] <= end_event['Timestamp'])
            data_df.loc[mask, 'Label'] = 'Blinking'

    # Save the labeled data to a new CSV file
    data_df.to_csv(output_csv, index=False)
