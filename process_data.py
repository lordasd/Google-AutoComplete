from collections import defaultdict
from typing import List
import re


class ProcessData:
    """
    Processes and manages text data for autocomplete functionality.

    This class handles the cleaning of text data, generation of substrings, and
    storage of processed information for efficient lookup during autocomplete operations.
    """

    def __init__(self):
        """
        Initializes the ProcessData instance with an empty defaultdict for storing data.
        """
        self.__data = defaultdict(list)
        self.__word_re = re.compile(r'\b[a-z]+\b')

    def get_all_substrings(self, words: List[str]):
        """
        Generates all possible substrings from a list of words.

        For each word, both prefixes and suffixes of length 2 up to the word's length
        are generated and added to the substring set.

        Parameters:
            words (List[str]): A list of words from which substrings are generated.

        Returns:
            set: A set of unique substrings.
        """
        sub_strings = set()
        for i in range(len(words)):
            n = len(words[i])
            for j in range(2, n+1):
                sub_strings.add(words[i][0:j])
                sub_strings.add(words[i][-j:n])
        return sub_strings

    def remove_punctuation(self, line):
        """
        Cleans a line of text by removing punctuation and converting to lowercase.

        Only alphabetical words are retained.

        Parameters:
            line (str): The input line to clean.

        Returns:
            str: The cleaned, lowercase version of the line without punctuation.
        """
        return ' '.join(self.__word_re.findall(line.lower()))


    def process(self, lines: List, filename: str):
        """
        Processes a list of lines from a text file and stores substrings with metadata.

        Each line is cleaned, substrings are generated, and the data is stored in the
        internal defaultdict along with the original line content, line number, and filename.

        Parameters:
            lines (List[str]): A list of lines from a text file.
            filename (str): The name of the file being processed.
        """

        for i in range(len(lines)):
            clean_line = self.remove_punctuation(lines[i].strip())

            if clean_line:
                sub_string = self.get_all_substrings(clean_line.split())
                for substring in sub_string:
                    self.__data[substring].append((lines[i], i+1, filename or "Unknown"))
        print("proccessed file", filename)


    def get_data(self):
        """
        Retrieves the processed data.

        Returns:
            defaultdict: A dictionary where keys are substrings and values are lists of tuples
                         containing the sentence, line number, and source filename.
        """
        return self.__data

    def set_data(self, data):
        """
        Sets the internal data with the provided data.

        Parameters:
            data (defaultdict): The processed data to be stored internally.
        """
        self.__data = data
