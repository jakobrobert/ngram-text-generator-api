import random

from ngram.ngram_prediction import NGramPrediction


class NGram:
    def __init__(self, history, prediction):
        self.history = history
        self.predictions = []
        self.predictions.append(NGramPrediction(prediction))

    def add_prediction(self, token):
        index = self.find_prediction_by_token(token)
        if index == -1:
            prediction = NGramPrediction(token)
            self.predictions.append(prediction)
        else:
            prediction = self.predictions[index]
            prediction.increment_frequency()

    def matches_history(self, history):
        if len(self.history) != len(history):
            return False
        for i in range(0, len(self.history)):
            if self.history[i] != history[i]:
                return False
        return True

    def pick_random_prediction(self):
        value = random.random()
        for prediction in self.predictions:
            if value < prediction.probability_threshold:
                return prediction.token
        return self.predictions[-1]

    # TODO Refactor: return prediction (or None) instead of index
    def find_prediction_by_token(self, token):
        for i in range(0, len(self.predictions)):
            if self.predictions[i].matches_token(token):
                return i
        return -1

    def calculate_probabilities(self):
        total_prediction_count = 0
        for prediction in self.predictions:
            total_prediction_count += prediction.frequency

        probability_threshold = 0.0
        for prediction in self.predictions:
            probability = prediction.frequency / total_prediction_count
            probability_threshold += probability
            prediction.probability = probability
            prediction.probability_threshold = probability_threshold
