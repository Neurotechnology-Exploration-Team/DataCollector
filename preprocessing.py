import pandas as pd

# Load event data
event_data = pd.read_csv('event_data.csv')
event_data['Timestamp'] = pd.to_datetime(event_data['Timestamp'])

# Load physiological data
phys_data = pd.read_csv('collected_data.csv')
phys_data['Timestamp'] = pd.to_datetime(phys_data['Timestamp'])

# Synchronize and merge data
# This example finds the nearest physiological data timestamp for each event
merged_data = pd.merge_asof(event_data.sort_values('Timestamp'), 
                            phys_data.sort_values('Timestamp'), 
                            on='Timestamp', 
                            direction='nearest')

# Save the merged data
merged_data.to_csv('merged_data.csv', index=False)

print("Data merging complete. Merged data saved to 'merged_data.csv'")