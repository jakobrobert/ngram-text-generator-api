from .ngram import NGram


class NGramModel:
    def __init__(self, order):
        self.order = order
        self.ngrams = []
        self.ngrams_by_history = {}

    def build_model_from_tokens(self, tokens):
        for i in range(0, len(tokens) - (self.order - 1)):
            history_end = i + self.order - 1
            history = tuple(tokens[i:history_end])
            prediction = tokens[history_end]

            ngram = self.find_ngram_by_history(history)
            if ngram is None:
                ngram = NGram(history)
                ngram.add_prediction(prediction)
                self.ngrams.append(ngram)
                self.ngrams_by_history[history] = ngram
            else:
                ngram.add_prediction(prediction)

        for ngram in self.ngrams:
            ngram.calculate_probabilities()

    def generate_tokens(self, start_history, length):
        tokens = start_history.copy()
        curr_history = tuple(start_history)

        while len(tokens) < length:
            ngram = self.find_ngram_by_history(curr_history)
            if ngram is None:
                return tokens

            prediction = ngram.pick_random_prediction()
            tokens.append(prediction)

            curr_history = tuple(tokens[-(self.order - 1):])

        return tokens

    @staticmethod
    def from_dict(data):
        order = data["order"]
        model = NGramModel(order)
        model.ngrams = [NGram.from_dict(ngram) for ngram in data["ngrams"]]
        model.ngrams_by_history = {}
        for ngram in model.ngrams:
            model.ngrams_by_history[ngram.history] = ngram
        return model

    def to_dict(self):
        return {
            "order": self.order,
            "ngrams": [ngram.to_dict() for ngram in self.ngrams]
        }

    def find_ngram_by_history(self, history):
        return self.ngrams_by_history.get(history, None)
