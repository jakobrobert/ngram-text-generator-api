from ngram.ngram import NGram


class NGramModel:
    def __init__(self, order):
        self.order = order
        self.ngrams = []

    def build_model_from_tokens(self, tokens):
        self.ngrams = []

        for i in range(0, len(tokens) - (self.order - 1)):
            # TODO Refactor: replace by slicing
            history = []
            for j in range(0, self.order - 1):
                history.append(tokens[i + j])
            prediction = tokens[i + self.order - 1]

            ngram = self.find_ngram_by_history(history)
            if ngram is None:
                self.ngrams.append(NGram(history, prediction))
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

    def to_dict(self):
        return {
            "order": self.order,
            "ngrams": [ngram.to_dict() for ngram in self.ngrams]
        }

    def find_ngram_by_history(self, history):
        for ngram in self.ngrams:
            if ngram.matches_history(history):
                return ngram
        return None
