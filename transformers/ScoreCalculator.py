class ScoreCalculator:

    def __init__(self):
        pass

    def fit(self, X=None, y=None):
        return self

    def transform(self, x):
        for problem in x:
            for error in problem.errors:
                for candidate in error.candidates:
                    candidate.score = candidate.similarity / candidate.distance
        return x
