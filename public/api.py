from flask import Flask, request, jsonify

from dictionary import Dictionary
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

    filtered_text = TextProcessor.filter_text(training_text)
    tokens = TextProcessor.tokenize(filtered_text)
    dictionary = TextProcessor.build_dictionary(tokens)
    token_ids = TextProcessor.convert_tokens_from_string_to_id(tokens, dictionary)

    model = NGramModel(order)
    model.build_model_from_tokens(token_ids)

    return jsonify(
        model=model.to_dict(),
        dictionary=dictionary.to_dict()
    )


@app.route("/ngram-text-generator-api/generate-text", methods=['POST'])
def generate_text():
    request_data = request.json
    start_text = request_data["start_text"]
    length = request_data["length"]
    model = NGramModel.from_dict(request_data["model"])
    dictionary = Dictionary.from_dict(request_data["dictionary"])

    start_history_tokens = TextProcessor.tokenize(start_text)
    start_history_ids = TextProcessor.convert_tokens_from_string_to_id(start_history_tokens, dictionary)
    token_ids = model.generate_tokens(start_history_ids, length)
    tokens = TextProcessor.convert_tokens_from_id_to_string(token_ids, dictionary)
    text = TextProcessor.concat_tokens_to_text(tokens)

    # TODO: replace dummy response by generated text
    return jsonify(
        text=text
    )


if __name__ == "__main__":
    # host 0.0.0.0 makes it publicly available
    app.run(host="0.0.0.0", port=4242, debug=True)
