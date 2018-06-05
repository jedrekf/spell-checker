import numpy as np


class ContextVectorizer:

    def __init__(self, model):
        self.model = model
        with open('stopwords.txt') as f:
            self.stopwords = f.readlines()
        self.stopwords = [x.strip() for x in self.stopwords]

    def fit(self, X=None, y=None):
        return self

    def transform(self, x):
        for problem in x:
            emb = []
            freqs = []
            for i, token in enumerate(problem.tokens):
                if not problem.is_error[i] and token not in self.stopwords:
                    emb.append(self.model.get_word_vector(token))
                    freqs.append(self.model.get_frequency(token))
            res = np.zeros(emb[0].shape)
            for idx, e in enumerate(emb):
                res = np.add(res, np.divide(e, freqs[idx]))
            problem.embeddings = res
        return x
