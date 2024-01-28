import argparse
import json
import os
parser = argparse.ArgumentParser(
    "generator token size most close to input -L|--length"
)
parser.add_argument("-T", "--tokenizer", type=str, required=True,
                        help="Path to the Tokenizer")
parser.add_argument("-I", "--input-length", type=int, required=True,
                        help="input token size")
parser.add_argument("-M", "--model", type=str, required=True,
                        help="model name")
parser.add_argument("-P", "--process-num", type=int, default=64,
                        help="process num, default is 64")
parser.add_argument("-O", "--max-tokens", type=int, default=500,
                        help="output length, default is 500")

if __name__ == "__main__":
    args = parser.parse_args()
    os.system(f"python3 gen.py -T {args.tokenizer} -L {args.input_length}")
    os.system(f"python3 run_single.py -M {args.model} -N {args.tokenizer} -D data/data_{args.input_length}.json -P {args.process_num} -L {args.max_tokens}")
