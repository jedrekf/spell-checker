from scipy import spatial
import numpy as np

class SimilarityCalculator:

    def __init__(self):
        pass

    def fit(self, X=None, y=None):
        return self

    def transform(self, x):
        for problem in x:
            for error in problem.errors:
                for candidate in error.candidates:
                    candidate.similarity = np.dot(candidate.embedding, problem.embeddings)/(np.linalg.norm(candidate.embedding)*np.linalg.norm(problem.embeddings))
        return x
