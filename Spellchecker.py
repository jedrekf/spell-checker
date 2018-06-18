from TextModel import TextModel
import transformers
from instances.ProblemInstance import ProblemInstance


class Spellchecker:

    def __init__(self, corpus_size=60000, max_dist=2, freq_weighting='natural', dist_weight=1):
        #freq_weighting possible values - 'natural', 'none', 'log'
        self.ft = TextModel()
        self.tokenizer = transformers.Tokenizer.Tokenizer().fit()
        self.error_detector = transformers.ErrorDetector.ErrorDetector(self.ft).fit()
        self.candidate_generator = transformers.TrieCandidateGenerator.\
            TrieCandidateGenerator(vocab_size=corpus_size, max_dist=max_dist, model=self.ft).fit()
        self.context_vectorizer = transformers.ContextVectorizer.ContextVectorizer(self.ft, freq_weighting).fit()
        self.candidate_vectorizer = transformers.CandidateVectorizer.CandidateVectorizer(self.ft).fit()
        self.similarity_calculator = transformers.SimilarityCalculator.SimilarityCalculator().fit()
        self.score_calculator = transformers.ScoreCalculator.\
            ScoreCalculator(distance_weight=dist_weight).fit()

    def transform(self, x):
        x = [ProblemInstance(y) for y in x]
        x = self.tokenizer.transform(x)
        x = self.error_detector.transform(x)
        x = self.candidate_generator.transform(x)
        x = self.context_vectorizer.transform(x)
        x = self.candidate_vectorizer.transform(x)
        x = self.similarity_calculator.transform(x)
        x = self.score_calculator.transform(x)
        return x

