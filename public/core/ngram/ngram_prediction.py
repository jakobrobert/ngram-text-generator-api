class NGramPrediction:
    def __init__(self, token, frequency=None, probability=None, probability_threshold=None):
        self.token = token
        self.frequency = frequency or 1
        self.probability = probability or 0.0
        self.probability_threshold = probability_threshold or 0.0

    # TODO inline these two functions, might improve performance
    def matches_token(self, token):
        return self.token == token

    def increment_frequency(self):
        self.frequency += 1

    @staticmethod
    def from_dict(data):
        prediction = NGramPrediction(data["token"])
        prediction.frequency = data["frequency"]
        prediction.probability = data["probability"]
        prediction.probability_threshold = data["probability_threshold"]
        return prediction

    def to_dict(self):
        return {
            "token": self.token,
            "frequency": self.frequency,
            "probability": self.probability,
            "probability_threshold": self.probability_threshold
        }
