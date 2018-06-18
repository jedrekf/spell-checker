import numpy as np


class ContextVectorizer:

    def __init__(self, model, freq_weighting="natural"):
        """

        :param model:
        :param freq_weighting: possible values - 'natural', 'log', 'none'
        """
        self.model = model
        self.weighting = freq_weighting
        with open('stopwords.txt') as f:
            self.stopwords = f.readlines()
        self.stopwords = [x.strip() for x in self.stopwords]

    def fit(self):
        return self

    def transform(self, x):
        for problem in x:
            emb = []
            freqs = []
            for i, token in enumerate(problem.tokens):
                if not problem.is_error[i] and token not in self.stopwords:
                    emb.append(self.model.get_word_vector(token))
                    freqs.append(self.model.get_frequency(token))
            if len(emb) == 0:
                emb.append(self.model.get_word_vector('aby'))
                freqs.append(self.model.get_frequency('aby'))
            res = np.zeros(emb[0].shape)
            for idx, e in enumerate(emb):
                if self.weighting == 'natural':
                    res = np.add(res, np.divide(e, freqs[idx]))
                elif self.weighting == 'log':
                    res = np.add(res, np.divide(e, np.log10(freqs[idx])))
                else:
                    res = np.add(res, e)
            problem.embeddings = res
        return x
