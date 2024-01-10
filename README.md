# NXT Data Collector

> This project houses the code to prompt the user in a Tkinter window, store, and process brain wave EEG data from an LSL stream.

### Current Version: [[1.0.1-a] - 1/9/2024](docs/changelog.md)

## Download & Install

### Git 

```bash
$ git clone https://github.com/Neurotechnology-Exploration-Team/DataCollector.git
$ cd DataCollector/
$ pip install -r requirements.txt
```

### Software Requirements
- Python v3.12.x
- [Standalone OpenBCI GUI](https://openbci.com/downloads) v5.2.2 (Required to interact with LSL stream data)
  - MacOS & Linux users will need to install [liblsl](https://github.com/sccn/liblsl); OpenBCI only ships with the library on Windows.

## Usage

> You will first need to setup LSL streams for the Data Collector to interface with.

### LSL Streaming

Launch **`OpenBCI_GUI.exe`**


Select data source type from **`System Control Panel > DATA SOURCE`**.
- Algorithmic LSL Data (Testing): Select **`SYNTHETIC (Algorithmic)`**
- ***TODO*** Real-Time LSL Data: Select **`CYTON (Live)`**


Leave all settings as default, and press **`START SESSION`**

Setup LSL Stream
- Change one of the widgets to **`Networking`**
- Change protocol to **`LSL`**
- Configure the Networking Window as follows:
> ![image](./docs/images/networking_configuration.png)

Press **`Start LSL Stream`** to activate the LSL stream on the local network. Press **`Start Data Stream`** to begin streaming test data.

> The LSL streams are now streaming on your laptop. Press **`Stop LSL Stream`** and **`Stop Data Stream`** when complete.

### Data Collection
> Once the LSL streams have been established, the data collection process can be initiated

Run main.py to run all tests and record data
```bash
$ python main.py
```

## Contributors
**Principal Investigator:** [Alex Burbano](mailto:arb8590@rit.edu)

**Research Team:**
- [Ian Dunn](mailto:itd3516@rit.edu)
- [Mack Leonard](mailto:mml2034@rit.edu)
- [Matt London](mailto:mrl2534@rit.edu)
