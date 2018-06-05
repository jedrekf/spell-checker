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

    ld.create_trie_list('./korpus.txt')

    start = time.time()
    results = ld.search('przejąc', 1)
    end = time.time()

    for result in results:
        print(result)

    print("Search took %g s" % (end - start))


ft = TextModel()
len(list(ft.get_corpus()))
x = [ProblemInstance(
         "W okresie w którym powstawała powieść tematyka chłopska była bartzo popularna w sztuce i literaturze"),
     ProblemInstance(
         "Bitwa ta zakończyła się zwycięstwem wojsc polsko-litewskich i pogromem sił krzyżackich, nie została jednak wykorzystana do całkowitego zniszczenia zakonu"),
    ProblemInstance('Istnieje kilka zachowanych źródeł dotyczących kitwy pod Grunwaldem i większość z nich zachowało się w polskich źródłach'),
    ProblemInstance('Najpopularniejszym gatunkiem uprawianym i spożywanym jest tomidor zwyczajny'),
    ProblemInstance('pomidor pomidor pomidor tomidor')]
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


