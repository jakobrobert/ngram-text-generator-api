from flask import Flask, request, jsonify
import json

app = Flask(__name__)


@app.route("/ngram-text-generator-api")
def index():
    return "Hello World!"


@app.route("/ngram-text-generator-api/build-model", methods=['POST'])
def build_model():
    request_data = request.json
    order = request_data["order"]
    training_text = request_data["training_text"]
    # TODO: replace dummy response by ngram model
    return jsonify(
        order=order,
        training_text=training_text
    )


@app.route("/ngram-text-generator-api/generate-text", methods=['POST'])
def generate_text():
    request_data = request.json
    start_text = request_data["start_text"]
    text_length = request_data["text_length"]
    model = request_data["model"]
    # TODO: replace dummy response by generated text
    return jsonify(
        start_text=start_text,
        text_length=text_length,
        model=model
    )


if __name__ == "__main__":
    # host 0.0.0.0 makes it publicly available
    app.run(host="0.0.0.0", port=4242, debug=True)
