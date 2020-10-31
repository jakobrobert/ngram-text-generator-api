from flask import Flask, request, jsonify

# special chars which are concatenated to the previous with a separation by space
SPECIAL_CHARS_WITH_SEPARATION = ["(", "[", "{", "\""]

# special chars which are directly concatenated to the previous token without any separation
SPECIAL_CHARS_WITHOUT_SEPARATION = [".", "?", "!", ",", ";", ":", ")", "]", "}", "\n"]

# all special chars, no distinction necessary for building the model
SPECIAL_CHARS = SPECIAL_CHARS_WITH_SEPARATION + SPECIAL_CHARS_WITHOUT_SEPARATION

app = Flask(__name__)

@app.route("/ngram-text-generator-api")
def index():
    return "Hello World!"


@app.route("/ngram-text-generator-api/build-model", methods=['POST'])
def build_model():
    request_data = request.json
    order = request_data["order"]
    training_text = request_data["training_text"]
    tokens = preprocess_text(training_text)
    # TODO: replace dummy response by ngram model
    return jsonify(
        order=order,
        tokens=tokens
    )


@app.route("/ngram-text-generator-api/generate-text", methods=['POST'])
def generate_text():
    request_data = request.json
    model = request_data["model"]
    start_text = request_data["start_text"]
    text_length = request_data["text_length"]
    # TODO: replace dummy response by generated text
    return jsonify(
        model=model,
        start_text=start_text,
        text_length=text_length
    )


def preprocess_text(text):
    filtered_text = filter_text(text)
    tokens = tokenize(filtered_text)
    # TODO: build dictionary
    return tokens


def filter_text(text):
    # remove all "\r" (carriage return)
    return text.replace("\r", "")


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
        elif text[current] in SPECIAL_CHARS:
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


if __name__ == "__main__":
    # host 0.0.0.0 makes it publicly available
    app.run(host="0.0.0.0", port=4242, debug=True)
