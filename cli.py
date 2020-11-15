import argparse


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

    print(args)


if __name__ == "__main__":
    main()
