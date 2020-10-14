from flask import Flask

app = Flask(__name__)


@app.route("/ngram-text-generator-api")
def index():
    return "Hello World!"


if __name__ == "__main__":
    # host 0.0.0.0 makes it publicly available
    app.run(host="0.0.0.0", port=4242, debug=True)
