import numpy as np


class ContextVectorizer:

    def __init__(self, model):
        self.model = model

    def fit(self, X=None, y=None):
        return self

    def transform(self, x):
        for problem in x:
            emb = []
            for i, token in enumerate(problem.tokens):
                if not problem.is_error[i]:
                    emb.append(self.model.get_word_vector(token))
            res = np.zeros(emb[0].shape)
            for e in emb:
                res = np.add(res, np.reciprocal(e))
            problem.embeddings = len(emb) * np.reciprocal(res)
        return x
