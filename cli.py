import argparse
import time

from public.core.ngram.ngram_model import NGramModel
from public.core.text_processor import TextProcessor

# imports for profiler
import cProfile
import pstats
import io


# decorator to profile a function
def profile(func):
    def inner(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        ret = func(*args, **kwargs)
        pr.disable()
        s = io.StringIO()
        sortby = "cumulative"
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())
        return ret
    return inner


def main():
    parser = argparse.ArgumentParser(description="Train an n-gram model based on a given text and generate a new text")
    required_args = parser.add_argument_group("required arguments")
    required_args.add_argument("-i", "--input", type=str, required=True,
                               help="Path to the input file containing the training text")
    required_args.add_argument("-o", "--output", type=str, required=True,
                               help="Path to the output file to store the generated text")
    required_args.add_argument("-r", "--order", type=int, required=True,
                               help="The order of the n-gram model")
    required_args.add_argument("-l", "--length", type=int, required=True,
                               help="The desired text length in tokens")
    required_args.add_argument("-s", "--start", type=str, required=False,
                               help="The start text as a coherent string, must be a (order-1)-gram which occurs\
                                   in the training text. Is optional, by default using first (order-1) tokens")
    args = parser.parse_args()

    input_path = args.input
    output_path = args.output
    order = args.order
    text_length = args.length
    start_text = args.start

    with open(input_path, "r", encoding="utf8") as file:
        training_text = file.read()

    model, dictionary = build_model(training_text, order)
    generated_text = generate_text(model, dictionary, text_length, start_text)

    with open(output_path, "w", encoding="utf8", newline="") as file:
        file.write(generated_text)


def build_model(training_text, order):
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

    return model, dictionary


def generate_text(model, dictionary, length, start_text):
    if start_text is None:
        start_history_ids = None
    else:
        start_history_tokens = TextProcessor.tokenize(start_text)
        start_history_ids = TextProcessor.convert_tokens_from_text_to_index(start_history_tokens, dictionary)

    start_time = time.perf_counter()
    token_indices = model.generate_tokens(length, start_history_ids)
    elapsed_time = int((time.perf_counter() - start_time) * 1000.0)
    print("Generate tokens (ms): " + str(elapsed_time))

    start_time = time.perf_counter()
    tokens = TextProcessor.convert_tokens_from_index_to_text(token_indices, dictionary)
    print("Generated text token count: " + str(len(tokens)))
    text = TextProcessor.concat_tokens_to_text(tokens)
    elapsed_time = int((time.perf_counter() - start_time) * 1000.0)
    print("Post-processing (ms): " + str(elapsed_time))

    return text


if __name__ == "__main__":
    main()
