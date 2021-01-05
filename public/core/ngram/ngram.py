import random

from .ngram_prediction import NGramPrediction


class NGram:
    def __init__(self, history, predictions=None):
        self.history = history
        self.predictions = predictions or []

    def add_prediction(self, token):
        prediction = self.find_prediction_by_token(token)
        if prediction is None:
            prediction = NGramPrediction(token)
            self.predictions.append(prediction)
        else:
            prediction.frequency += 1

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
        history = tuple(data["history"])
        ngram = NGram(history)
        ngram.predictions = [NGramPrediction.from_dict(prediction) for prediction in data["predictions"]]
        return ngram

    def to_dict(self):
        return {
            "history": self.history,
            "predictions": [prediction.to_dict() for prediction in self.predictions]
        }

    def find_prediction_by_token(self, token):
        for prediction in self.predictions:
            if prediction.token == token:
                return prediction
        return None
