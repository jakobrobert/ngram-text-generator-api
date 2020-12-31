class Dictionary:
    def __init__(self, token_indices_by_text=None, token_texts_by_index=None):
        self.token_indices_by_text = token_indices_by_text or {}
        self.token_texts_by_index = token_texts_by_index or {}
        self.curr_token_index = 0

    # TODO might optimize by method add_tokens to reduce function calls
    def add_token(self, text):
        if text in self.token_indices_by_text:
            return
        self.token_indices_by_text[text] = self.curr_token_index
        self.token_texts_by_index[self.curr_token_index] = text
        self.curr_token_index += 1

    def token_index_by_text(self, text):
        return self.token_indices_by_text[text]

    def token_text_by_index(self, index):
        return self.token_texts_by_index[index]

    @staticmethod
    def from_dict(data):
        dictionary = Dictionary()
        dictionary.token_indices_by_text = data["token_indices_by_text"]
        dictionary.token_texts = data["token_texts_by_index"]
        return dictionary

    def to_dict(self):
        return {
            "token_indices_by_text": self.token_indices_by_text,
            "token_texts_by_index": self.token_texts_by_index
        }
