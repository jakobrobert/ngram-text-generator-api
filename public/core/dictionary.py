class Dictionary:
    def __init__(self, token_indices_by_text=None, token_texts=None):
        self.token_indices_by_text = token_indices_by_text or {}
        self.token_texts = token_texts or []

    # TODO might optimize by method add_tokens to reduce function calls
    def add_token(self, text):
        if text in self.token_indices_by_text:
            return
        # the index corresponds to the current number of tokens
        self.token_indices_by_text[text] = len(self.token_texts)
        self.token_texts.append(text)

    def token_index_by_text(self, text):
        return self.token_indices_by_text[text]

    def token_text_by_index(self, index):
        return self.token_texts[index]

    @staticmethod
    def from_dict(data):
        dictionary = Dictionary()
        dictionary.token_indices_by_text = data["token_indices_by_text"]
        dictionary.token_texts = data["token_texts"]
        return dictionary

    def to_dict(self):
        return {
            "token_indices_by_text": self.token_indices_by_text,
            "token_texts": self.token_texts
        }
