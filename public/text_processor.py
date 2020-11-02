from dictionary import Dictionary


class TextProcessor:
    # special chars which are concatenated to the previous with a separation by space
    SPECIAL_CHARS_WITH_SEPARATION = ["(", "[", "{", "\""]

    # special chars which are directly concatenated to the previous token without any separation
    SPECIAL_CHARS_WITHOUT_SEPARATION = [".", "?", "!", ",", ";", ":", ")", "]", "}", "\n"]

    # all special chars, no distinction necessary for building the model
    SPECIAL_CHARS = SPECIAL_CHARS_WITH_SEPARATION + SPECIAL_CHARS_WITHOUT_SEPARATION

    def __init__(self):
        self.dictionary = None

    def filter_text(self, text):
        # remove all "\r" (carriage return)
        return text.replace("\r", "")

    def tokenize(self, text):
        tokens = []
        current = 0
        token_start = 0

        while current < len(text):
            if text[current] == " ":
                # take string before space as token (only if not empty)
                if token_start < current:
                    token = text[token_start:current]
                    tokens.append(token)
                # skip space
                current += 1
                token_start = current
            elif text[current] in TextProcessor.SPECIAL_CHARS:
                # take string before special char as token (only if not empty)
                if token_start < current:
                    token = text[token_start:current]
                    tokens.append(token)
                # add special char as separate token
                special_char = text[current]
                tokens.append(special_char)
                current += 1
                token_start = current
            else:
                # no new token found, just continue with next char
                current += 1

        # add remaining part as last token (only if not empty)
        if token_start < len(text):
            token = text[token_start:]
            tokens.append(token)

        return tokens

    def build_dictionary(self, tokens):
        self.dictionary = Dictionary()
        for token in tokens:
            self.dictionary.add_token(token)

    def convert_tokens_to_ids(self, tokens):
        ids = []
        for token in tokens:
            id_ = self.dictionary.id_of_token(token)
            ids.append(id_)
        return ids
