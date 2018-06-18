#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import nltk.data
import re
from DatasetGenerator import DataSet
import json
import preprocess

# from DatasetGenerator import DataSet

# use this to download data for tokenizer for splitting sentences
# import nltk
# nltk.download('punkt')

args = sys.argv[1:]

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

corpus_path = args[0] if len(args) > 0 else '/home/jedrek/Downloads/processed_messages.json'
do_preprocess_str = args[1] if len(args) > 1 else "False"
do_preprocess = do_preprocess_str in ['True', 'true', '1', 't', 'y', 'yes', 'yeah', 'preprocess']

text = open(corpus_path, encoding='us-ascii').read()
data = json.loads(text)
sentences = [x['sentence'] for x in data]

processed_sentences = []
if do_preprocess:
    for sentence in sentences:
        processed_sentences.append(preprocess.polish(sentence))
    
    sentences = processed_sentences

print(sentences[:10])

sentences = '\n'.join(sentences)
output_file = 'shopy_sentences_korpus.txt'
with open(output_file, 'w') as the_file:
    the_file.write(sentences)
