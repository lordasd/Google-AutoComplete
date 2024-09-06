class AutoCompleteData:
    """
    Represents an autocomplete suggestion with associated metadata.

    Attributes:
        completed_sentence (str): The suggested completed sentence.
        source_text (str): The filename from which the suggestion originates.
        offset (int): The line number in the source file where the sentence is located.
        score (int): The relevance score of the suggestion (default is 0).
    """

    def __init__(self, completed_sentence: str, source_text: str, offset: int, score: int = 0):
        """
        Initializes the AutoCompleteData instance with sentence details.

        Parameters:
            completed_sentence (str): The suggested completed sentence.
            source_text (str): The filename where the sentence was found.
            offset (int): The line number in the file.
            score (int, optional): The relevance score of the suggestion. Defaults to 0.
        """
        self.__completed_sentence = completed_sentence
        self.__source_text = source_text
        self.__offset = offset
        self.__score = score

    def __str__(self):
        """
        Returns a string representation of the autocomplete suggestion.

        Returns:
            str: A formatted string containing the sentence, source filename, and line number.
        """
        return f" {self.__completed_sentence} (Filename: {self.__source_text} Line: {self.__offset})"
