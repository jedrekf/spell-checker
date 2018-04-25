class CandidateInstance:

    def __init__(self, word, distance):
        self.word = word
        self.embedding = None
        self.distance = distance
        self.similarity = None
        self.score = None
