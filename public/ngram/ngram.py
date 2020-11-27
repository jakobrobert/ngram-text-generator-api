import random

from .ngram_prediction import NGramPrediction


class NGram:
    def __init__(self, history):
        self.history = history
        self.predictions = []

    def add_prediction(self, token):
        index = self.find_prediction_by_token(token)
        if index == -1:
            prediction = NGramPrediction(token)
            self.predictions.append(prediction)
        else:
            prediction = self.predictions[index]
            prediction.increment_frequency()

    def pick_random_prediction(self):
        value = random.random()
        for prediction in self.predictions:
            if value < prediction.probability_threshold:
                return prediction.token
        return self.predictions[-1]

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

    @staticmethod
    def from_dict(data):
        history = data["history"]
        ngram = NGram(history)
        ngram.predictions = [NGramPrediction.from_dict(prediction) for prediction in data["predictions"]]
        return ngram

    def to_dict(self):
        return {
            "history": self.history,
            "predictions": [prediction.to_dict() for prediction in self.predictions]
        }

    # TODO Refactor: return prediction (or None) instead of index
    def find_prediction_by_token(self, token):
        for i in range(0, len(self.predictions)):
            if self.predictions[i].matches_token(token):
                return i
        return -1
