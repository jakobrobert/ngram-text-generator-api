import argparse

from public.ngram.ngram_model import NGramModel
from public.text_processor import TextProcessor


def main():
    parser = argparse.ArgumentParser(description="Train an n-gram model based on a given text and generate a new text")
    required_args = parser.add_argument_group("required arguments")
    required_args.add_argument("-i", "--input", type=str, required=True,
                               help="Path to the input file containing the training text")
    required_args.add_argument("-o", "--output", type=str, required=True,
                               help="Path to the output file to store the generated text")
    required_args.add_argument("-r", "--order", type=int, required=True,
                               help="The order of the n-gram model")
    required_args.add_argument("-s", "--start", type=str, required=True,
                               help="The start text as a coherent string, must be a (order-1)-gram which occurs\
                               in the training text")
    required_args.add_argument("-l", "--length", type=int, required=True,
                               help="The desired text length in tokens")
    args = parser.parse_args()

    input_path = args.input
    output_path = args.output
    order = args.order
    start_text = args.start
    text_length = args.length

    with open(input_path, "r", encoding="utf8") as file:
        training_text = file.read()

    model = build_model(training_text, order)
    print(model.to_dict())


def build_model(training_text, order):
    filtered_text = TextProcessor.filter_text(training_text)
    tokens = TextProcessor.tokenize(filtered_text)
    dictionary = TextProcessor.build_dictionary(tokens)
    token_ids = TextProcessor.convert_tokens_from_string_to_id(tokens, dictionary)

    model = NGramModel(order)
    model.build_model_from_tokens(token_ids)

    return model


if __name__ == "__main__":
    main()
