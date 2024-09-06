import string
import random
import re
from auto_complete_data import AutoCompleteData
from collections import defaultdict
from typing import List, Tuple, Optional


class AutoComplete:
    """
    Provides autocomplete functionality based on processed data.

    This class offers methods to generate autocomplete suggestions by manipulating
    input queries and matching them against a processed dataset.
    """

    def __init__(self, ht: defaultdict):
        """
        Initializes the AutoComplete instance with processed data.

        Parameters:
            ht (defaultdict): A dictionary containing substrings as keys and lists of
                             tuples with sentence data as values.
        """
        self.ht = ht
        self.__word_re = re.compile(r'\b[a-z]+\b')

    def create_auto_complete(self, lines: List[Tuple[str, int, str]]) -> List[AutoCompleteData]:
        """
        Converts raw line data into AutoCompleteData instances.

        Parameters:
            lines (List[Tuple[str, int, str]]): A list of tuples containing sentence,
                                                line number, and source filename.

        Returns:
            List[AutoCompleteData]: A list of AutoCompleteData instances.
        """
        responses = []
        for i in range(len(lines)):
            responses.append(
                AutoCompleteData(
                    lines[i][0],  # completed_sentence
                    lines[i][2],  # source_text
                    lines[i][1]  # offset
                ))
        return responses

    def delete_char(self, sentence: str) -> List[Tuple[str, int]]:
        """
        Generates possible sentences by deleting one character at each position.

        Parameters:
            sentence (str): The input sentence from which characters will be deleted.

        Returns:
            List[Tuple[str, int]]: A list of tuples containing the modified sentence and its score.
        """
        score = (len(sentence) - 1) * 2
        valid_sentences = []

        for i in range(len(sentence), -1, -1):
            new_sentence = sentence[:i] + sentence[i + 1:]
            if new_sentence in self.ht:
                penalty = max(10 - 2 * i, 2)  # Adjusts the score based on the position
                new_score = score - penalty
                valid_sentences.append((new_sentence, new_score))
                if len(valid_sentences) == 5:
                    break

        return valid_sentences

    def addition_score(self, index: int, max_score: int) -> int:
        """
        Calculates the score for adding a character based on its position.

        Parameters:
            index (int): The position at which the character is added.
            max_score (int): The maximum possible score before penalty.

        Returns:
            int: The adjusted score after applying the penalty.
        """
        penalties = [10, 8, 6, 4]
        return max_score - (penalties[index] if index < 4 else 2)

    def add_char(self, sentence: str) -> List[Tuple[str, int]]:
        """
        Generates possible sentences by adding one character at each position.

        Parameters:
            sentence (str): The input sentence to which characters will be added.

        Returns:
            List[Tuple[str, int]]: A list of tuples containing the modified sentence and its score.
        """
        n = len(sentence)
        res = []
        for char in range(ord('a'), ord('z') + 1):
            for i in range(n, -1, -1):
                cur_word = sentence[:i] + chr(char) + sentence[i:]
                if cur_word in self.ht:
                    res.append((cur_word, self.addition_score(i, n * 2)))
        return res

    def has_multiple_mismatches(self, subtext: str) -> bool:
        """
        Determines if the subtext contains more than one word not present in the dataset.

        Parameters:
            subtext (str): The input subtext to check for mismatches.

        Returns:
            bool: True if there are multiple mismatched words, False otherwise.
        """

        mismatches = 0
        for word in subtext.split():
            if word not in self.ht:
                mismatches += 1
                if mismatches > 1:  # We don't allow words with an error of more than one letter.
                    return True
        return False

    def find_mismatched_word_and_index(self, subtext: str) -> Optional[Tuple[str, int]]:
        """
        Identifies the first mismatched word in the subtext and its starting index.

        Parameters:
            subtext (str): The input subtext to search for mismatches.

        Returns:
            Optional[Tuple[str, int]]: A tuple containing the mismatched word and its index,
                                       or None if no mismatches are found.
        """

        for i, word in enumerate(subtext.split()):
            if word not in self.ht:
                return word, i
        return None

    def generate_possible_replacements(self, mismatched_word: str, subtext: str, end_word_index: int) -> List[Tuple[str, int]]:
        """
        Generates possible replacements for a mismatched word by altering its characters.

        Parameters:
            mismatched_word (str): The word identified as mismatched.
            subtext (str): The entire subtext containing the mismatched word.
            end_word_index (int): The ending index of the mismatched word in the subtext.

        Returns:
            List[Tuple[str, int]]: A list of tuples containing possible replacement words and their scores.
        """
        # 2 points fot each suitable char.
        score = (len(subtext) - 1) * 2
        alphabet = string.ascii_lowercase
        possible_words = []

        for i in range(len(mismatched_word), -1, -1):
            for char in alphabet:
                if char == subtext[end_word_index - i]:
                    continue

                new_word = subtext[:end_word_index - i] + char + subtext[end_word_index - i + 1:]
                if new_word in self.ht:
                    penalty = 1 if (end_word_index - i) > 3 else 5 - (end_word_index - i)
                    new_score = score - penalty
                    possible_words.append((new_word, new_score))
                    if len(possible_words) == 5:
                        break

        return possible_words

    def replace_char(self, subtext: str) -> List[Tuple[str, int]]:
        """
        Attempts to correct the subtext by replacing a single character in a mismatched word.

        Parameters:
            subtext (str): The input subtext to correct.

        Returns:
            List[Tuple[str, int]]: A list of corrected subtexts and their scores.
        """

        if self.has_multiple_mismatches(subtext):
            return []

        mismatched_word, start_index = self.find_mismatched_word_and_index(subtext)

        end_word_index = start_index + len(mismatched_word) - 1
        return self.generate_possible_replacements(mismatched_word, subtext, end_word_index)

    def get_best_completions(self, subtext: str) -> Optional[str]:
        """
        Combines various character manipulations to find the best autocomplete suggestion.

        Parameters:
            subtext (str): The input subtext for which to find completions.

        Returns:
            Optional[str]: The best matching sentence or None if no match is found.
        """

        combining_list = self.replace_char(subtext) + self.delete_char(subtext) + self.add_char(subtext)
        higher = float('-inf')
        found_key = ""
        for combination in combining_list:
            if combination[1] > higher:
                higher = combination[1]
                found_key = combination[0]

        return found_key

    def check_if_input_in_line(self, user_input_words: List[str], line_words: List[str]) -> bool:
        """
        Checks if the user input words appear sequentially within a line of words.

        Parameters:
            user_input_words (List[str]): The list of words from the user's input.
            line_words (List[str]): The list of words from a line in the dataset.

        Returns:
            bool: True if the input words are found sequentially in the line, False otherwise.
        """
        for i, word in enumerate(line_words):
            if user_input_words[0] in word:
                j, k = 0, i
                while j < len(user_input_words) and k < len(line_words):
                    if user_input_words[j] not in line_words[k]:
                        return False
                    j += 1
                    k += 1

                if j == len(user_input_words):
                    return True
        return False

    def get_best_k_completion(self, user_input: str, k: int = 5) -> List[AutoCompleteData]:
        """
        Retrieves the top K autocomplete suggestions based on user input.

        Parameters:
            user_input (str): The input string provided by the user.
            k (int): The maximum number of suggestions to return (default is 5).

        Returns:
            List[AutoCompleteData]: A list of autocomplete suggestions.
        """

        user_words = self.__word_re.findall(user_input.lower().strip())
        lines = set()
        correct_sentence = []

        # Find lines that contain all the words in the input sentence and intersect them
        for word in user_words:
            if word in self.ht:
                if len(lines) == 0:
                    lines = set(self.ht[word])
                else:
                    lines.intersection_update(self.ht[word])
                correct_sentence.append(word)
            else:
                new_word = self.get_best_completions(word)
                if new_word:
                    if len(lines) == 0:
                        lines = set(self.ht[new_word])
                    else:
                        lines.intersection_update(self.ht[new_word])
                    correct_sentence.append(new_word)
                else:
                    return []

        final_lines = []
        if len(user_words) > 1:
            for line in lines:
                line_words = self.__word_re.findall(line[0].lower().strip())
                if self.check_if_input_in_line(correct_sentence, line_words):
                    final_lines.append(line)
        else:
            final_lines = list(lines)

        if len(final_lines) > k:
            random_elements = random.sample(final_lines, k)
            return self.create_auto_complete(random_elements)
        else:
            return self.create_auto_complete(final_lines)
          