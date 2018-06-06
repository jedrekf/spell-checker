import fastText
import config as cfg

class TextModel:

    def __init__(self):
        self.model = fastText.FastText.load_model(cfg.MODEL_PATH)
        self.corpus = self.model.get_words(include_freq=True)

    def is_in_dict(self, x):
        return x in self.model.get_words()

    def get_word_vector(self, x):
        return self.model.get_word_vector(x)

    def get_corpus(self, size=60000):
        return self.corpus[0][:size]

    def get_frequency(self, word):
        if word in self.corpus[0]:
            return self.corpus[1][self.corpus[0].index(word)]
        else:
            return 204774366




