from .dictionary import Dictionary


class TextProcessor:
    # special chars which are concatenated to the previous with a separation by space
    SPECIAL_CHARS_WITH_SEPARATION = ["(", "[", "{", "\""]

    # special chars which are directly concatenated to the previous token without any separation
    SPECIAL_CHARS_WITHOUT_SEPARATION = [".", "?", "!", ",", ";", ":", ")", "]", "}", "\n"]

    # all special chars, no distinction necessary for building the model
    SPECIAL_CHARS = SPECIAL_CHARS_WITH_SEPARATION + SPECIAL_CHARS_WITHOUT_SEPARATION

    @staticmethod
    def filter_text(text):
        # remove all "\r" (carriage return)
        return text.replace("\r", "")

    @staticmethod
    def tokenize(text):
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

    @staticmethod
    def build_dictionary(tokens):
        dictionary = Dictionary()
        dictionary.build_from_tokens(tokens)
        return dictionary

    @staticmethod
    def convert_tokens_from_text_to_index(token_texts, dictionary):
        token_indices = []
        for token_text in token_texts:
            token_index = dictionary.token_indices_by_text[token_text]
            token_indices.append(token_index)
        return token_indices

    @staticmethod
    def convert_tokens_from_index_to_text(token_indices, dictionary):
        token_texts = []
        for token_index in token_indices:
            token_text = dictionary.token_texts_by_index[token_index]
            token_texts.append(token_text)
        return token_texts

    @staticmethod
    def concat_tokens_to_text(tokens):
        if len(tokens) == 0:
            return ""

        text = tokens[0]

        for i in range(1, len(tokens)):
            curr_token = tokens[i]
            prev_token = tokens[i - 1]
            if curr_token in TextProcessor.SPECIAL_CHARS_WITHOUT_SEPARATION:
                text += curr_token
            else:
                # for both cases, special chars with separation and normal words, separate by space
                # but only if previous token was not a special char with separation
                # e.g. "bla (hello)" should separate "(" by space, but not "hello"
                if prev_token not in TextProcessor.SPECIAL_CHARS_WITH_SEPARATION:
                    text += " "
                text += curr_token

        return text
