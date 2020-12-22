class Dictionary:
    def __init__(self):
        self.token_ids_by_text = {}
        self.token_texts_by_id = {}
        self.next_token_id = 0

    # TODO might optimize by method add_tokens to reduce function calls
    def add_token(self, text):
        if text in self.token_ids_by_text:
            return
        id_ = self.next_token_id
        self.next_token_id += 1
        self.token_ids_by_text[text] = id_
        self.token_texts_by_id[id_] = text

    def token_id_by_text(self, text):
        return self.token_ids_by_text[text]

    def token_text_by_id(self, id_):
        return self.token_texts_by_id[id_]

    @staticmethod
    def from_dict(data):
        dictionary = Dictionary()
        dictionary.token_ids_by_text = data["token_ids_by_text"]
        dictionary.token_texts_by_id = data["token_texts_by_id"]
        return dictionary

    def to_dict(self):
        return {
            "token_ids_by_text": self.token_ids_by_text,
            "token_texts_by_id": self.token_texts_by_id
        }
