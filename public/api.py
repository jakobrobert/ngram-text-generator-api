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
    print("JSON deserialization (ms): " + str(elapsed_time))

    start_time = time.perf_counter()
    filtered_text = TextProcessor.filter_text(training_text)
    tokens = TextProcessor.tokenize(filtered_text)
    print("Training text token count: " + str(len(tokens)))
    dictionary = TextProcessor.build_dictionary(tokens)
    token_indices = TextProcessor.convert_tokens_from_text_to_index(tokens, dictionary)
    elapsed_time = int((time.perf_counter() - start_time) * 1000.0)
    print("Pre-processing (ms): " + str(elapsed_time))

    start_time = time.perf_counter()
    model = NGramModel(order)
    model.build_model_from_tokens(token_indices)
    elapsed_time = int((time.perf_counter() - start_time) * 1000.0)
    print("Build model (ms): " + str(elapsed_time))

    start_time = time.perf_counter()
    database = Database()
    model_id = database.add_model(model)
    print("model id: " + str(model_id))
    database.add_dictionary_to_model(dictionary, model_id)
    elapsed_time = int((time.perf_counter() - start_time) * 1000.0)
    print("Database serialization (ms): " + str(elapsed_time))

    start_time = time.perf_counter()

    response = jsonify(
        model_id=model_id
    )
    elapsed_time = int((time.perf_counter() - start_time) * 1000.0)
    print("JSON serialization (ms): " + str(elapsed_time))

    return response


@app.route("/ngram-text-generator-api/generate-text", methods=['POST'])
def generate_text():
    start_time = time.perf_counter()
    request_data = request.json
    model_id = request_data["model_id"]
    length = request_data["length"]
    if "start_text" in request_data:
        start_text = request_data["start_text"]
    else:
        start_text = None
    elapsed_time = int((time.perf_counter() - start_time) * 1000.0)
    print("JSON deserialization (ms): " + str(elapsed_time))

    start_time = time.perf_counter()
    database = Database()
    model = database.get_model(model_id)
    dictionary = database.get_dictionary_from_model(model_id)
    elapsed_time = int((time.perf_counter() - start_time) * 1000.0)
    print("Database deserialization (ms): " + str(elapsed_time))

    if start_text is None:
        start_history_indices = None
    else:
        start_history_tokens = TextProcessor.tokenize(start_text)
        start_history_indices = TextProcessor.convert_tokens_from_text_to_index(start_history_tokens, dictionary)

    start_time = time.perf_counter()
    token_ids = model.generate_tokens(length, start_history_indices)
    elapsed_time = int((time.perf_counter() - start_time) * 1000.0)
    print("Generate tokens (ms): " + str(elapsed_time))

    start_time = time.perf_counter()
    tokens = TextProcessor.convert_tokens_from_index_to_text(token_ids, dictionary)
    print("Generated text token count: " + str(len(tokens)))
    text = TextProcessor.concat_tokens_to_text(tokens)
    elapsed_time = int((time.perf_counter() - start_time) * 1000.0)
    print("Post-processing (ms): " + str(elapsed_time))

    start_time = time.perf_counter()
    response = jsonify(
        text=text
    )
    elapsed_time = int((time.perf_counter() - start_time) * 1000.0)
    print("JSON serialization (ms): " + str(elapsed_time))

    return response


if __name__ == "__main__":
    # host 0.0.0.0 makes it publicly available
    app.run(host="0.0.0.0", port=4242, debug=True)
