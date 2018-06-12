class ProblemInstance:

    def __init__(self, sentence):
        self.sentence = sentence
        self.tokens = []
        self.errors = []
        self.embeddings = None
        self.is_error = []

    def get_corrected_sentence(self):
        for error in self.errors:
            if len(error.candidates) > 0 and error.candidates is not None:
                candidate = sorted(error.candidates, key=lambda x: x.score, reverse=True)[0]
                self.tokens[error.index] = candidate.word
        return ' '.join(self.tokens)
