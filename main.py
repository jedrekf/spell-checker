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

def main(argv):

    ld = LevenshteinDistance()

    ld.create_trie_list('./korpus.txt')

    start = time.time()
    results = ld.search('przejąc', 1)
    end = time.time()

    for result in results:
        print(result)

    print("Search took %g s" % (end - start))

'''
ft = TextModel()
len(list(ft.get_corpus()))

x = Tokenizer().fit().transform(x)
x = ErrorDetector(ft).fit().transform(x)
x = TrieCandidateGenerator(model=ft).fit().transform(x)
x = ContextVectorizer(ft).fit().transform(x)
x = CandidateVectorizer(ft).fit().transform(x)
x = SimilarityCalculator().fit().transform(x)
x = ScoreCalculator().fit().transform(x)
#y = WordReplacer().fit().transform(x)
#print(y)
for instance in x:
    for error in instance.errors:
        print(error.word)
        for candidate in sorted(error.candidates, key=lambda z: z.score):
            print(candidate.word, candidate.score, candidate.similarity, candidate.distance)
'''
x = []
y = []
with open('invalid_sentences_korpus.txt') as f:
    x = f.readlines()
    x = [z.strip() for z in x]
    x = [''.join(ch for ch in z if (ch.isalnum()) or ch == ' ') for z in x]
with open('sentences_korpus.txt') as f:
    y = f.readlines()
    y = [z.strip() for z in y]
    y = [''.join(ch for ch in z if (ch.isalnum()) or ch == ' ') for z in y]
x = x[:300]
y = y[:300]
word_count = 0
error_count = 0
correction_count = 0
detected_count = 0
sp = Spellchecker()
results = sp.transform(x)
corrections = []
for idx, instance in enumerate(results):
    for error in instance.errors:
        print(error.word)
        for candidate in sorted(error.candidates, key=lambda z: z.score):
            print(candidate.word, candidate.score, candidate.similarity, candidate.distance)
    correct = y[idx].lower().split(' ')
    corrected = instance.get_corrected_sentence().lower().split(' ')
    wrong = x[idx].lower().split(' ')
    for token in zip(correct, wrong, corrected, instance.is_error):
        word_count = word_count + 1
        if token[0] != token[1]:
            error_count = error_count + 1
            if token[0] == token[2]:
                correction_count = correction_count + 1
            if token[3]:
                detected_count = detected_count + 1
            corrections.append(token)
print(correction_count)
print(detected_count)
print(error_count)
print(word_count)
with open('results.csv', 'w') as out:
    csv_out = csv.writer(out)
    for row in corrections:
        csv_out.writerow(row)
