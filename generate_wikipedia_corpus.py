#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import nltk.data
from xml.dom import minidom
import re
from DatasetGenerator import DataSet

# from DatasetGenerator import DataSet

# use this to download data for tokenizer for splitting sentences
# import nltk
# nltk.download('punkt')

args = sys.argv[1:]

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

corpus_path = args[0] if len(args) > 0 else '/home/jedrek/Downloads/plwiki3_1/'
sentences = []
subdir_count = 0

for subdir, dirs, files in os.walk(corpus_path):
    subdir_count += 1

cleanr = re.compile('<.*?>')

for counter, (subdir, dirs, files) in enumerate(os.walk(corpus_path)):
    # if name contains only numbers the set doesn't contain errors
    print(subdir)
    print("%: " + str((counter/subdir_count)*100) )
    for file in files:
        text = open(subdir+'/'+file, encoding='utf-8').read()
        text = re.sub(cleanr, '', text)
        lines = text.split('\n')
        new_sentences = tokenizer.tokenize(' '.join(lines))
        new_sentences = [s for s in new_sentences if len(s)>5]
        sentences = sentences + new_sentences

print(sentences[:10])

sentences = '\n'.join(sentences)
temp_file = 'wiki_sentences_korpus.temp.txt'
with open(temp_file, 'w') as the_file:
    the_file.write(sentences)

dataset = DataSet('wiki_sentences_korpus.temp.txt', inverted=False)
# os.remove(temp_file)

print("questions")
print(dataset.questions_train[:2])
print("answers")
print(dataset.answers[:2])

output_question_file = args[1] if len(args)>1 else 'wiki_invalid_sentences_korpus.txt'
with open(output_question_file, 'w') as the_file:
    the_file.write("\n".join(dataset.questions_train))

output_answer_file = args[2] if len(args)>2 else 'wiki_sentences_korpus.txt'
with open(output_answer_file, 'w') as the_file:
    the_file.write("\n".join(dataset.answers))
