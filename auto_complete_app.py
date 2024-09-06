import os
import pickle

from auto_complete import AutoComplete
from zip_opener import ZipOpener
from process_data import ProcessData


class AutoCompleteApp:
    """
    The main application class for the AutoComplete functionality.

    This class handles the initialization, data processing, and user interaction
    required to provide autocomplete suggestions based on a dataset of text files.
    """

    def __init__(self):
        """
        Initializes the AutoCompleteApp instance.

        Currently, no initialization parameters are required.
        """
        pass

    def save_data_to_file(self, data_processor):
        """
        Serializes and saves processed data to a file using pickle.

        Parameters:
            data_processor (ProcessData): The data processor containing processed data.
        """
        print("Saving data to a file... Please wait.")
        with open("data.pkl", "wb") as file:
            pickle.dump(data_processor.get_data(), file)
        print("Saved data successfully.")

    def load_data_from_file(self, data_processor):
        """
        Loads serialized data from a file and deserializes it using pickle.

        Parameters:
            data_processor (ProcessData): The data processor to populate with loaded data.
        """
        print("Loading processed data from file... Please wait.")
        with open("data.pkl", "rb") as file:
            data_processor.set_data(pickle.load(file))

    def user_interaction(self, data_processor):
        """
        Handles the interactive user session for autocomplete suggestions.

        Parameters:
            data_processor (ProcessData): The data processor containing processed data.
        """
        auto_complete = AutoComplete(data_processor.get_data())
        current_query = ""

        print("Hello! You can start searching:")
        print("To start a new sentence, enter '#'. To exit, type '#exit'.")

        while True:
            query = input(f"{current_query}")
            if query.lower() == '#exit':
                break
            elif query == '#':
                current_query = ""
                continue
            else:
                current_query += query

            # Retrieve autocomplete results based on the current query
            results = auto_complete.get_best_k_completion(current_query.strip().lower())

            # Display up to 5 autocomplete suggestions
            for i in range(len(results)):
                print(f'({i + 1}) {results[i]}')

        print("Goodbye!")

    def start(self):
        """
        Initiates the AutoComplete application workflow.

        This includes data processing, loading or saving processed data, and
        starting the user interaction loop.
        """
        zip_opener = ZipOpener('dataset.zip')
        data_processor = ProcessData()

        # Check if processed data exists; if not, process and save it
        if not os.path.exists("data.pkl"):
            print("Processing data... Please wait.")
            zip_opener.read(data_processor)
            self.save_data_to_file(data_processor)
        else:
            self.load_data_from_file(data_processor)

        print("Data processed successfully.\n\n")

        # Start the interactive autocomplete session
        self.user_interaction(data_processor)
