class NGramPrediction:
    def __init__(self, token):
        self.token = token
        self.frequency = 1
        self.probability = 0.0
        self.probability_threshold = 0.0

    # TODO Inline these two functions, might improve performance
    def matches_token(self, token):
        return self.token == token

    def increment_frequency(self):
        self.frequency += 1

    @staticmethod
    def from_dict(data):
        token = data["token"]
        prediction = NGramPrediction(token)
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
