from flask import Flask, request, jsonify

from text_processor import TextProcessor

app = Flask(__name__)


@app.route("/ngram-text-generator-api")
def index():
    return "Hello World!"


@app.route("/ngram-text-generator-api/build-model", methods=['POST'])
def build_model():
    request_data = request.json
    order = request_data["order"]
    training_text = request_data["training_text"]

    # TODO: merge into one function, currently separated into intermediate results for debugging
    processor = TextProcessor()
    filtered_text = processor.filter_text(training_text)
    tokens = processor.tokenize(filtered_text)
    processor.build_dictionary(tokens)
    token_ids = processor.convert_tokens_to_ids(tokens)

    # TODO: replace debug response by ngram model
    return jsonify(
        order=order,
        training_text=training_text,
        filtered_text=filtered_text,
        tokens=tokens,
        token_ids=token_ids
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


if __name__ == "__main__":
    # host 0.0.0.0 makes it publicly available
    app.run(host="0.0.0.0", port=4242, debug=True)
