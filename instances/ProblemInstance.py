class ProblemInstance:

    def __init__(self, sentence):
        self.sentence = sentence
        self.tokens = []
        self.errors = []
        self.embeddings = None