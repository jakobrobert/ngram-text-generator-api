from flask import Flask, request, jsonify
import time

from core.dictionary import Dictionary
from core.ngram.ngram_model import NGramModel
from core.text_processor import TextProcessor

from database import Database

app = Flask(__name__)


@app.route("/ngram-text-generator-api/build-model", methods=['POST'])
def build_model():
    start_time = time.perf_counter()
    request_data = request.json
    order = request_data["order"]
    training_text = request_data["training_text"]
    elapsed_time = int((time.perf_counter() - start_time) * 1000.0)
    print("Deserialization (ms): " + str(elapsed_time))

    start_time = time.perf_counter()
    filtered_text = TextProcessor.filter_text(training_text)
    tokens = TextProcessor.tokenize(filtered_text)
    print("Training text token count: " + str(len(tokens)))
    dictionary = TextProcessor.build_dictionary(tokens)
    token_ids = TextProcessor.convert_tokens_from_string_to_id(tokens, dictionary)
    elapsed_time = int((time.perf_counter() - start_time) * 1000.0)
    print("Pre-processing (ms): " + str(elapsed_time))

    start_time = time.perf_counter()
    model = NGramModel(order)
    model.build_model_from_tokens(token_ids)
    elapsed_time = int((time.perf_counter() - start_time) * 1000.0)
    print("Build model (ms): " + str(elapsed_time))

    start_time = time.perf_counter()
    response = jsonify(
        model=model.to_dict(),
        dictionary=dictionary.to_dict(),
        token_count=len(tokens)
    )
    elapsed_time = int((time.perf_counter() - start_time) * 1000.0)
    print("Serialization (ms): " + str(elapsed_time))

    # TODO database test code, remove after integration
    database = Database()
    model_id = database.add_model(model)
    print("model")
    print(database.get_model(model_id).to_dict())
    database.add_dictionary(dictionary)
    print("dictionary")
    print(database.get_dictionary().to_dict())

    return response


@app.route("/ngram-text-generator-api/generate-text", methods=['POST'])
def generate_text():
    start_time = time.perf_counter()
    request_data = request.json
    model = NGramModel.from_dict(request_data["model"])
    dictionary = Dictionary.from_dict(request_data["dictionary"])
    length = request_data["length"]
    if "start_text" in request_data:
        start_text = request_data["start_text"]
    else:
        start_text = None

    elapsed_time = int((time.perf_counter() - start_time) * 1000.0)
    print("Deserialization (ms): " + str(elapsed_time))

    if start_text is None:
        start_history_ids = None
    else:
        start_history_tokens = TextProcessor.tokenize(start_text)
        start_history_ids = TextProcessor.convert_tokens_from_string_to_id(start_history_tokens, dictionary)

    start_time = time.perf_counter()
    token_ids = model.generate_tokens(length, start_history_ids)
    elapsed_time = int((time.perf_counter() - start_time) * 1000.0)
    print("Generate tokens (ms): " + str(elapsed_time))

    start_time = time.perf_counter()
    tokens = TextProcessor.convert_tokens_from_id_to_string(token_ids, dictionary)
    print("Generated text token count: " + str(len(tokens)))
    text = TextProcessor.concat_tokens_to_text(tokens)
    elapsed_time = int((time.perf_counter() - start_time) * 1000.0)
    print("Post-processing (ms): " + str(elapsed_time))

    start_time = time.perf_counter()
    response = jsonify(
        text=text,
        token_count=len(tokens)
    )
    elapsed_time = int((time.perf_counter() - start_time) * 1000.0)
    print("Serialization (ms): " + str(elapsed_time))

    return response


if __name__ == "__main__":
    # host 0.0.0.0 makes it publicly available
    app.run(host="0.0.0.0", port=4242, debug=True)
