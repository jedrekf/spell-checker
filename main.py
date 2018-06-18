import time
import sys
import csv

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
    start_time = datetime.datetime.now()
    x = []
    y = []
    with open('wiki_invalid_sentences_korpus.txt') as f:
        x = f.readlines()
        x = [z.strip() for z in x]
        x = [''.join(ch for ch in z if (ch.isalnum()) or ch == ' ') for z in x]
    with open('wiki_sentences_korpus.txt') as f:
        y = f.readlines()
        y = [z.strip() for z in y]
        y = [''.join(ch for ch in z if (ch.isalnum()) or ch == ' ') for z in y]
    word_count = 0
    error_count = 0
    correction_count = 0
    detected_count = 0
    sp = Spellchecker(freq_weighting='log', dist_weight=0.4, corpus_size=10**5)
    for i in range(0, len(x), 100):
        try:
            end_idxx = min(len(x), i+100)
            results = sp.transform(x[i:end_idxx])
            corrections = []
            for idx, instance in enumerate(results):
                correct = y[i+idx].lower().split(' ')
                corrected = instance.get_corrected_sentence().lower().split(' ')
                wrong = x[i+idx].lower().split(' ')
                for token in zip(correct, wrong, corrected, instance.is_error):
                    word_count = word_count + 1
                    if token[0] != token[1]:
                        error_count = error_count + 1
                        if token[0] == token[2]:
                            correction_count = correction_count + 1
                        if token[3]:
                            detected_count = detected_count + 1
                        corrections.append(token)
            print('Batch number: '+str(i))
            print(correction_count)
            print(detected_count)
            print(error_count)
            print(word_count)
            with open('results_'+str(start_time)+'.csv', 'a') as out:
                csv_out = csv.writer(out)
                for row in corrections:
                    csv_out.writerow(row)
        except:
            with open('error.log', 'a') as myfile:
                myfile.write('Error at batch: '+i+'\n')
 

if __name__ == "__main__":
    main()