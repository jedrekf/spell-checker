class WordReplacer:

    def __init__(self):
        pass

    def fit(self, x=None, y=None):
        return self

    def transform(self, x):
        results = []
        for problem in x:
            for error in problem.errors:
                max_score = max([e.score for e in error.candidates])
                best_candidates = [c for c in error.candidates if c.score == max_score]
                problem.tokens[error.index] = best_candidates[0].word.lower()
            results.append(" ".join(problem.tokens))
        return results