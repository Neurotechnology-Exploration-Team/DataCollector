import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter
fs = 250.0
lowcut = 1.0  
highcut = 50.0  


def butter_bandpass_filter(data, order=5):
	def butter_bandpass(order=5):
		nyq = 0.5 * fs
		low = lowcut / nyq
		high = highcut / nyq
		b, a = butter(order, [low, high], btype='band')
		return b, a
	b, a = butter_bandpass(order=order)
	y = lfilter(b, a, data)
	return y

if __name__ == "__main__":
	csv_file = 'data/collected_data.csv' 
	eeg_data = pd.read_csv(csv_file)


	channel_name = 'EEG_4'
	eeg_channel = eeg_data[channel_name].values

	filtered_signal = butter_bandpass_filter(eeg_channel, order=6)

