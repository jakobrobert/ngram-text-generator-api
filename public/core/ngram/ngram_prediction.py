class NGramPrediction:
    # TODO optional arg to directly pass probability and probability threshold
    def __init__(self, token_index):
        self.token_index = token_index
        self.frequency = 1
        self.probability = 0.0
        self.probability_threshold = 0.0

    # TODO inline these two functions, might improve performance
    def matches_token(self, token_index):
        return self.token_index == token_index

    def increment_frequency(self):
        self.frequency += 1

    @staticmethod
    def from_dict(data):
        prediction = NGramPrediction(data["token_index"])
        prediction.frequency = data["frequency"]
        prediction.probability = data["probability"]
        prediction.probability_threshold = data["probability_threshold"]
        return prediction

    def to_dict(self):
        return {
            "token_index": self.token_index,
            "frequency": self.frequency,
            "probability": self.probability,
            "probability_threshold": self.probability_threshold
        }
