class Dictionary:
    def __init__(self, token_indices_by_text=None, token_texts_by_index=None):
        self.token_indices_by_text = token_indices_by_text or {}
        self.token_texts_by_index = token_texts_by_index or {}
        self.curr_token_index = 0

    def build_from_tokens(self, token_texts):
        for text in token_texts:
            if text not in self.token_indices_by_text:
                self.token_indices_by_text[text] = self.curr_token_index
                self.token_texts_by_index[self.curr_token_index] = text
                self.curr_token_index += 1

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
