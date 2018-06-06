class ScoreCalculator:

    def __init__(self, distance_weight=1):
        self.weight = distance_weight

    def fit(self, X=None, y=None):
        return self

    def transform(self, x):
        for problem in x:
            for error in problem.errors:
                for candidate in error.candidates:
                    candidate.score = candidate.similarity / \
                        (candidate.distance * self.weight)
        return x
