# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.1.0-a] - 1/17/2024

### Added
- Popup when initializing GUI to prompt for the subject number.

## [3.0.0-a] - 1/16/2024

### Added

- `config` file in the repository root directory that holds all experiment/collection constants.
- Button colors to indicate test status

### Changed

- Changed `tests` package to a class-based system that uses Python's default `Thread` class.
  - Each test is now a class that extends the `TestThread` class, which holds logic that applies to all tests.
  - Moved all Tkinter logic into `tests/TestGUI` static class.
- Converted `LSL` module to a static class.
- Labelling is now performed entirely in the `LSL` class

### Fixed
- Multiple confirmation window bugs

## [2.0.0-a] - 1/9/2024

### Added

- Lots of docstrings, documentation, code cleanup, etc.

### Changed

- Changed `lsl.py` module to the `LSL.py` class, allowing for one instance of LSL to manipulate.
- Moved most constants to the top-level of relevant modules.

## [1.0.1-a] - 1/9/2024

### Changed

- Update `requirements.txt` to be the minimum required packages to install.

## [1.0.0-a] - 1/9/2024

### Added

- `changelog.md` to keep track of changes.
- All LSL & post-processing functionality.
- Tests using Tkinter windows.

### Fixed

- No LSL stream would hang up the program instead of exiting.

### Changed

### Removed

