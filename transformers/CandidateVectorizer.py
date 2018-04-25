class CandidateVectorizer:

    def __init__(self, model):
        self.model = model

    def fit(self, x=None, y=None):
        return self

    def transform(self, x):
        for problem in x:
            for error in problem.errors:
                for candidate in error.candidates:
                    candidate.embedding = self.model.get_word_vector(candidate.word)
        return x
