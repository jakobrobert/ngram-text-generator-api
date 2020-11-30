from .ngram import NGram

import numpy as np


class NGramModel:
    def __init__(self, order):
        self.order = order
        self.ngrams = []

    def build_model_from_tokens(self, tokens):
        self.ngrams = []
        np_tokens = np.array(tokens, dtype=np.int_)

        for i in range(0, len(np_tokens) - (self.order - 1)):
            history_end = i + self.order - 1
            history = np_tokens[i:history_end]
            prediction = np_tokens[history_end]

            ngram = self.find_ngram_by_history(history)
            if ngram is None:
                ngram = NGram(history)
                ngram.add_prediction(prediction)
                self.ngrams.append(ngram)
            else:
                ngram.add_prediction(prediction)

        for ngram in self.ngrams:
            ngram.calculate_probabilities()

    def generate_tokens(self, start_history, length):
        tokens = start_history.copy()
        curr_history = start_history

        while len(tokens) < length:
            ngram = self.find_ngram_by_history(curr_history)
            if ngram is None:
                return tokens

            prediction = ngram.pick_random_prediction()
            tokens.append(prediction)

            curr_history = tokens[-(self.order - 1):]

        return tokens

    @staticmethod
    def from_dict(data):
        order = data["order"]
        model = NGramModel(order)
        model.ngrams = [NGram.from_dict(ngram) for ngram in data["ngrams"]]
        return model

    def to_dict(self):
        return {
            "order": self.order,
            "ngrams": [ngram.to_dict() for ngram in self.ngrams]
        }

    def find_ngram_by_history(self, history):
        for ngram in self.ngrams:
            if (ngram.history == history).all():
                return ngram
        return None
