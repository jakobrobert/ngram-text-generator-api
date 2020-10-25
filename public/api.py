from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/ngram-text-generator-api")
def index():
    return "Hello World!"


# TODO: change to POST with json body
# TODO: return ngram model as json
@app.route("/ngram-text-generator-api/build-model", methods=['GET'])
def build_model():
    order = int(request.args.get('order'))
    training_text = request.args.get('training-text')
    return jsonify(
        order=order,
        training_text=training_text
    )


# TODO: change to POST with json body
# TODO: provide ngram model as json
@app.route("/ngram-text-generator-api/generate-text", methods=['GET'])
def generate_text():
    start_text = request.args.get("start-text")
    text_length = int(request.args.get("text-length"))
    return jsonify(
        start_text=start_text,
        text_length=text_length
    )


if __name__ == "__main__":
    # host 0.0.0.0 makes it publicly available
    app.run(host="0.0.0.0", port=4242, debug=True)
