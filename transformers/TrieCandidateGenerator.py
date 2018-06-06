from trie.levenshtein_distance import LevenshteinDistance
import config as cfg
from instances.CandidateInstance import CandidateInstance


class TrieCandidateGenerator:
    def __init__(self, vocab_size, max_dist=2, model=None):
        self.tree = LevenshteinDistance(model)
        self.max_dist = max_dist
        self.model = model
        self.vocab_size = vocab_size

    def fit(self, x=None, y=None):
        self.tree.create_trie_list(self.model.get_corpus(self.vocab_size))
        return self

    def transform(self, x):
        for problem in x:
            for error in problem.errors:
                results = self.tree.search(error.word, self.max_dist)
                for word, cost in results:
                    error.candidates.append(CandidateInstance(word, cost))
        return x

