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

corpus_path = args[0] if len(args) > 0 else '/home/piotr/Downloads/corpus'
sentences = []
for subdir, dirs, files in os.walk(corpus_path):
    # if name contains only numbers the set doesn't contain errors
    print(subdir)
    foldername = subdir.split('/')[-1]
    if foldername is '':
        foldername = "a"

    result = re.search("[a-zA-Z]", foldername)

    if result is None:
        # its good we take it
        xmldoc=minidom.parse(subdir + '/text.xml')
        for node in xmldoc.getElementsByTagName('ab'):
            node_text = node.firstChild.nodeValue
            node_sentences = tokenizer.tokenize(node_text)
            node_sentences = [s for s in new_sentences if len(s)>5]
            sentences = sentences + node_sentences

print(sentences[:10])

sentences = '\n'.join(sentences)
temp_file = 'nkjp_sentences_korpus.temp.txt'
with open(temp_file, 'w') as the_file:
    the_file.write(sentences)

dataset = DataSet('nkjp_sentences_korpus.temp.txt', inverted=False)
os.remove(temp_file)

print("questions")
print(dataset.questions_train[:2])
print("answers")
print(dataset.answers[:2])

output_question_file = args[1] if len(args)>1 else 'nkjp_invalid_sentences_korpus.txt'
with open(output_question_file, 'w') as the_file:
    the_file.write("\n".join(dataset.questions_train))

output_answer_file = args[2] if len(args)>2 else 'nkjp_sentences_korpus.txt'
with open(output_answer_file, 'w') as the_file:
    the_file.write("\n".join(dataset.answers))
