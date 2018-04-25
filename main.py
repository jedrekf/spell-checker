import time
import sys

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

def main(argv):

    ld = LevenshteinDistance()

    ld.create_trie('./korpus.txt')

    start = time.time()
    results = ld.search('przejąc', 1)
    end = time.time()

    for result in results:
        print(result)

    print("Search took %g s" % (end - start))


ft = TextModel()
x = [ProblemInstance("W okresie w którym powstawała powieść tematyka chłopska była wardzo popularna w sztuce i literaturze"),
     ProblemInstance(
         "W okresie w którym powstawała powieść tematyka chłopska była bartzo popularna w sztuce i literaturze"),
     ProblemInstance(
         "W okresie w którym powstawała powieść tematyka chłopska była barzo popularna w sztuce i literaturze")]
x = Tokenizer().fit().transform(x)
x = ErrorDetector(ft).fit().transform(x)
x = TrieCandidateGenerator().fit().transform(x)
x = ContextVectorizer(ft).fit().transform(x)
x = CandidateVectorizer(ft).fit().transform(x)
x = SimilarityCalculator().fit().transform(x)
x = ScoreCalculator().fit().transform(x)
y = WordReplacer().fit().transform(x)
print(y)

