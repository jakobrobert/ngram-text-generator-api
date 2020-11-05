from flask import Flask, request, jsonify

from ngram.ngram_model import NGramModel
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

    model = NGramModel(order)
    model.build_model_from_tokens(token_ids)

    return jsonify(model.to_dict())


@app.route("/ngram-text-generator-api/generate-text", methods=['POST'])
def generate_text():
    request_data = request.json
    start_text = request_data["start_text"]
    text_length = request_data["text_length"]
    model_data = request_data["model"]

    # TODO: generate text
    model = NGramModel.from_dict(model_data)

    # TODO: replace dummy response by generated text
    return jsonify(
        start_text=start_text,
        text_length=text_length,
        model=model.to_dict(),
        text="Test"
    )


if __name__ == "__main__":
    # host 0.0.0.0 makes it publicly available
    app.run(host="0.0.0.0", port=4242, debug=True)
