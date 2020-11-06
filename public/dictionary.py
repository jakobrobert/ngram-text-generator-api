class Dictionary:
    def __init__(self):
        self.token_ids = {}
        self.tokens = []

    def add_token(self, token):
        if token in self.token_ids:
            return
        self.token_ids[token] = len(self.tokens)    # use current number of tokens as ID of this token
        self.tokens.append(token)

    def id_of_token(self, token):
        return self.token_ids[token]

    def token_by_id(self, id_):
        return self.tokens[id_]

    @staticmethod
    def from_dict(data):
        dictionary = Dictionary()
        dictionary.token_ids = data["token_ids"]
        dictionary.tokens = data["tokens"]
        return dictionary

    def to_dict(self):
        return {
            "token_ids": self.token_ids,
            "tokens": self.tokens
        }
