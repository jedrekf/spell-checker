# encoding: utf-8

from collections import Counter
import re
import numpy as np
from numpy.random import choice as random_choice
from numpy.random import randint as random_randint
from numpy.random import shuffle as random_shuffle
from numpy.random import rand
from numpy import zeros as np_zeros  # pylint:disable=no-name-in-module
from time import time

# Parameters for the model and dataset
MAX_INPUT_LEN = 100
MIN_INPUT_LEN = 3
AMOUNT_OF_NOISE = 0.6 / 100
# NUMBER_OF_CHARS = 100  # 75
CHARS = list("aąbcćdeęfghijklłmnńoópqrsśtuvwxyzźżAĄBCĆDEĘFGHIJKLŁMNŃOÓPQRSŚTUVWXYZŹŻ .")

# Some cleanup:
NORMALIZE_WHITESPACE_REGEX = re.compile(r'[^\S\n]+', re.UNICODE)  # match all whitespace except newlines
RE_DASH_FILTER = re.compile(r'[\-\˗\֊\‐\‑\‒\–\—\⁻\₋\−\﹣\－]', re.UNICODE)
RE_APOSTROPHE_FILTER = re.compile(r'&#39;|[ʼ՚＇‘’‛❛❜ߴߵ`‵´ˊˋ{}{}{}{}{}{}{}{}{}]'.format(
                                        chr(768), chr(769), chr(832), chr(833), chr(2387), chr(5151),
                                        chr(5152), chr(65344), chr(8242)),
                                    re.UNICODE)
RE_LEFT_PARENTH_FILTER = re.compile(r'[\(\[\{\⁽\₍\❨\❪\﹙\（]', re.UNICODE)
RE_RIGHT_PARENTH_FILTER = re.compile(r'[\)\]\}\⁾\₎\❩\❫\﹚\）]', re.UNICODE)
ALLOWED_CURRENCIES = """¥£₪$€฿₨"""
ALLOWED_PUNCTUATION = """-!?/;"'%&<>.()[]{}@#:,|=*"""
RE_BASIC_CLEANER = re.compile(r'[^\w\s{}{}]'.format(
                                    re.escape(ALLOWED_CURRENCIES), re.escape(ALLOWED_PUNCTUATION)),
                                re.UNICODE)


class DataSet(object):
    """
    Loads news articles from a file, generates misspellings and vectorizes examples.
    """

    def __init__(self, dataset_filename, inverted=True):
        
        self.inverted = inverted

        news = self.read_news(dataset_filename)
        MAX_INPUT_LEN = max(news, key=len)
        questions, answers = self.generate_examples(news)

        chars_answer = set.union(*(set(answer) for answer in answers))
        chars_question = set.union(*(set(question) for question in questions))
        self.chars = sorted(list(set.union(chars_answer, chars_question)))

        self.questions_train = questions
        self.answers = answers

        self.x_max_length = max(len(question) for question in questions)
        self.y_max_length = max(len(answer) for answer in answers)


        print("Completed pre-processing")

    def add_noise_to_string(self, a_string, amount_of_noise):
        """Add some artificial spelling mistakes to the string"""
        if rand() < amount_of_noise * len(a_string):
            # Replace a character with a random character
            random_char_position = random_randint(len(a_string))
            a_string = a_string[:random_char_position] + random_choice(CHARS[:-1]) + a_string[random_char_position + 1:]
        if rand() < amount_of_noise * len(a_string):
            # Delete a character
            random_char_position = random_randint(len(a_string))
            a_string = a_string[:random_char_position] + a_string[random_char_position + 1:]
        if len(a_string) < MAX_INPUT_LEN and rand() < amount_of_noise * len(a_string):
            # Add a random character
            random_char_position = random_randint(len(a_string))
            a_string = a_string[:random_char_position] + random_choice(CHARS[:-1]) + a_string[random_char_position:]
        if rand() < amount_of_noise * len(a_string):
            # Transpose 2 characters
            random_char_position = random_randint(len(a_string) - 1)
            a_string = (a_string[:random_char_position] +
                        a_string[random_char_position + 1] +
                        a_string[random_char_position] +
                        a_string[random_char_position + 2:])
        return a_string

    def clean_text(self, text):
        """Clean the text - remove unwanted chars, fold punctuation etc."""

        text = text.strip()
        text = NORMALIZE_WHITESPACE_REGEX.sub(' ', text)
        text = RE_DASH_FILTER.sub('-', text)
        text = RE_APOSTROPHE_FILTER.sub("'", text)
        text = RE_LEFT_PARENTH_FILTER.sub("(", text)
        text = RE_RIGHT_PARENTH_FILTER.sub(")", text)
        text = RE_BASIC_CLEANER.sub('', text)

        return text

    def read_news(self, dataset_filename):
        """Read the news corpus"""
        print("Reading news")
        news = open(dataset_filename, encoding='utf-8').read()
        print("Read news")

        lines = [line for line in news.split('\n')]
        print("Read {} lines of input corpus".format(len(lines)))

        lines = [self.clean_text(line) for line in lines]
        print("Cleaned text")

        counter = Counter()
        for line in lines:
            counter += Counter(line)

        # most_popular_chars = {key for key, _value in counter.most_common(NUMBER_OF_CHARS)}
        # print(most_popular_chars)

        # lines = [line for line in lines if line and not bool(set(line) - most_popular_chars)]
        # print("Left with {} lines of input corpus".format(len(lines)))

        return lines

    def generate_examples(self, corpus):
        """Generate examples of misspellings"""

        print("Generating examples")

        questions, answers = [], corpus

        # print('Shuffle')
        # random_shuffle(answers)
        # print("Shuffled")

        for answer_index, answer in enumerate(answers):
            question = self.add_noise_to_string(answer, AMOUNT_OF_NOISE)
            # question += '.' * (MAX_INPUT_LEN - len(question))
            # answer += "." * (MAX_INPUT_LEN - len(answer))
            answers[answer_index] = answer
            # assert len(answer) == MAX_INPUT_LEN

            question = question[::-1] if self.inverted else question
            questions.append(question)

        print("Generated questions and answers")

        return questions, answers