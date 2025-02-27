﻿# Google AutoComplete Project

## Overview
This project implements an autocomplete system similar to Google’s autocomplete feature. It reads a large dataset of text files, processes the data, and provides intelligent suggestions for text completion based on user input. The core functionality involves manipulating sentences by deleting, adding, or replacing characters and retrieving the most relevant completions using a scoring system.

## Features
- **Autocomplete Suggestions**: Provides top `k` autocomplete suggestions for a given input based on processed text files.
- **Character Manipulations**: Generates suggestions by deleting, adding, or replacing characters in the input.
- **Efficient Data Lookup**: Processes and stores substrings from text files to offer fast lookups during autocomplete operations.
- **Interactive User Session**: A command-line interface allows users to interact with the autocomplete system and view suggestions in real-time.

## Authors
- **David Zaydenberg** - [DavidZdbr@gmail.com](mailto:DavidZdbr@gmail.com)
- **Adi Yakoby** - [adi.yakoby@gmail.com](mailto:adi.yakoby@gmail.com)

## Requirements
- Python 3.8+
- Required Libraries:
  - `re`
  - `string`
  - `pickle`
  - `collections`
  - `random`
  - `zipfile`

## Project Structure
```
.
├── app.py                 # Entry point for the application
├── auto_complete.py       # Core logic for generating autocomplete suggestions
├── auto_complete_app.py   # Main application workflow handling data processing and user interaction
├── auto_complete_data.py  # Data model for storing autocomplete suggestion metadata
├── process_data.py        # Class for processing and managing dataset text files
├── zip_opener.py          # Utility for reading and extracting text files from a ZIP archive
├── dataset.zip            # A zip file containing text files used for autocomplete
└── data.pkl               # Serialized processed data (created after initial processing)
```

## How It Works
1. **Data Preprocessing**:
   - The application reads `.txt` files from `dataset.zip` using the `ZipOpener` class.
   - The `ProcessData` class processes the content of each file, cleaning the text and extracting all possible substrings from sentences.
   - Substrings are stored in a `defaultdict`, allowing efficient lookups during autocomplete operations.

2. **Autocomplete Logic**:
   - The `AutoComplete` class provides methods to manipulate input sentences:
     - **Character Deletion**: Removes a character and checks if the modified sentence exists in the dataset.
     - **Character Addition**: Adds characters at various positions and checks for valid sentences.
     - **Character Replacement**: Replaces characters in the input to find possible sentence corrections.
   - A scoring system is applied to each modification to prioritize the most relevant suggestions.

3. **User Interaction**:
   - The user can input partial queries in the command line, and the app will return up to 5 autocomplete suggestions.
   - The user can reset the current query by entering `#` or exit the session by typing `#exit`.

4. **Data Persistence**:
   - After the first run, the processed data is saved as a `data.pkl` file using `pickle`, so subsequent runs can load the data directly, skipping the processing step.

## Running the Project

1. **Install Requirements**:
   Ensure you have the required Python version and libraries installed. You can install the dependencies using the following command:
   ```bash
   pip install -r requirements.txt
   ```

2. **Execute the Application**:
   Run the following command to start the autocomplete system:
   ```bash
   python app.py
   ```

3. **User Interaction**:
   - Start typing your query and get real-time autocomplete suggestions.
   - **To start a new sentence, enter `#`.**
   - **To exit the application, type `#exit`.**

## Example Usage
```bash
Hello! You can start searching:
To start a new sentence, enter '#'. To exit, type '#exit'.
apple p
(1) apple pie is delicious. (Filename: example.txt Line: 4)
(2) apple pancakes are the best. (Filename: example.txt Line: 12)
```

## Data Flow
1. **Input Data**: The application reads `.txt` files from `dataset.zip`.
2. **Processing**: The `ProcessData` class extracts substrings from sentences and stores them for fast retrieval.
3. **Autocomplete Suggestions**: The `AutoComplete` class uses various methods (character manipulation, scoring, etc.) to generate autocomplete suggestions based on user input.
4. **Output**: Up to 5 of the best suggestions are displayed to the user.

## Future Enhancements
- **Web Interface**: Implement a web-based user interface using Flask or Django for a more interactive experience.
- **Optimized Scoring**: Refine the scoring mechanism to improve the relevance of suggestions.
- **Support for Large Datasets**: Introduce multi-threading or distributed processing for handling very large text corpora efficiently.

## License
This project is licensed under the MIT License.
