# NXT Data Collector
> This project houses the code to prompt the user in a Tkinter window, store, and process brain wave EEG data from an LSL stream.

## Download & Install

### Git 
```bash
$ git clone https://github.com/Neurotechnology-Exploration-Team/DataCollector.git
$ cd DataCollector/
$ pip install -r requirements.txt
```

### OpenBCI GUI
> This is required to interact with LSL stream data.

Install the latest version of the [Standalone OpenBCI GUI](https://openbci.com/downloads) (v5.2.2)


## Usage
> You will first need to setup an LSL stream for the Data Collector to interface with.

### LSL Streaming

1. Launch `OpenBCI_GUI.exe`
2. Select data source type from from `System Control Panel > DATA SOURCE`.
   1. **Algorithmic LSL Data (Testing):** Select **`SYNTHETIC (Algorithmic)`** 
   2. **Real-Time LSL Data:** Select **`CYTON (Live)`** (?)
3. Leave all settings as default, and press `START SESSION`
4. Press `Start Data Stream` to begin streaming test data.

> The synthetic data is now streaming. Press `Stop Data Stream` when complete.

### Data Collection

## Contributors
**Principal Investigator:** [Alex Burbano](mailto:arb8590@rit.edu)

**Research Team:**
- [Ian Dunn](mailto:itd3516@rit.edu)