#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import nltk.data
from DatasetGenerator import DataSet

# use this to download data for tokenizer for splitting sentences
# import nltk
# nltk.download('punkt')

args = sys.argv[1:]

input_file = args[0] if len(args)>0 else 'book.txt'
with open(input_file, 'r') as myfile:
    lines = myfile.read().splitlines()

# remove standalone numbers as lines and remove conversation lines
lines = [line for line in lines if ((' ' in line) and (line[0] != "—"))]
text = " ".join(lines)

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
sentences = '\n'.join(tokenizer.tokenize(text))

output_file = args[1] if len(args)>1 else 'sentences_korpus.temp.txt'
with open(output_file, 'w') as the_file:
    the_file.write(sentences)

dataset = DataSet('sentences_korpus.temp.txt', inverted=False)
os.remove('sentences_korpus.temp.txt')

print("questions")
print(dataset.questions_train[:2])
print("answers")
print(dataset.answers[:2])

output_question_file = args[1] if len(args)>1 else 'invalid_sentences_korpus.txt'
with open(output_question_file, 'w') as the_file:
    the_file.write("\n".join(dataset.questions_train))

output_answer_file = args[2] if len(args)>2 else 'sentences_korpus.txt'
with open(output_answer_file, 'w') as the_file:
    the_file.write("\n".join(dataset.answers))

