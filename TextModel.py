import fastText
import config as cfg

class TextModel:
    def __init__(self):
        self.model = fastText.FastText.load_model(cfg.MODEL_PATH)

    def is_in_dict(self, x):
        return x in self.model.get_words()

    def get_word_vector(self, x):
        return self.model.get_word_vector(x)