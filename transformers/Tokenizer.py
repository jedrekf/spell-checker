import fastText


class Tokenizer:
    def __init__(self):
        pass

    def fit(self, x=None, y=None):
        return self

    def transform(self, x):
        for instance in x:
            instance.tokens = fastText.FastText.tokenize(instance.sentence.lower())
        return x

