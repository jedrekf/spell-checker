import time
import sys
import csv
import fastText
import os

from TextModel import TextModel
from instances.ProblemInstance import ProblemInstance
from transformers.Tokenizer import Tokenizer
from transformers.ErrorDetector import ErrorDetector
from trie.levenshtein_distance import LevenshteinDistance
from transformers.TrieCandidateGenerator import TrieCandidateGenerator
from transformers.ContextVectorizer import ContextVectorizer
from transformers.CandidateVectorizer import CandidateVectorizer
from transformers.ScoreCalculator import ScoreCalculator
from transformers.SimilarityCalculator import SimilarityCalculator
from transformers.WordReplacer import WordReplacer
from Spellchecker import Spellchecker
import datetime

def main():
    if(len(sys.argv) < 2):
        print('Please enter the path to input file as command line argument')
    start_time = datetime.datetime.now()
    input_file = sys.argv[1]
    x = []
    with open(input_file) as f:
        x = f.readlines()
        x = [z.strip() for z in x]
        x = [''.join(ch for ch in z if (ch.isalnum()) or ch == ' ') for z in x]
    word_count = 0
    error_count = 0
    correction_count = 0
    detected_count = 0
    sp = Spellchecker(freq_weighting='log', dist_weight=0.7, corpus_size=10**5)
    for i in range(0, len(x), 100):
        end_idxx = min(len(x), i+100)
        results = sp.transform(x[i:end_idxx])
        corrections = []
        for idx, instance in enumerate(results):
            corrections.append(instance.get_corrected_sentence())
        with open('results_'+str(start_time)+'.txt', 'a') as out:
            for row in corrections:
                out.write(row)
                out.write(os.linesep)
 

if __name__ == "__main__":
    main()