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
