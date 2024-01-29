import argparse
import json
import os
parser = argparse.ArgumentParser(
    "generator token size most close to input -L|--length"
)
parser.add_argument("-T", "--tokenizer", type=str, required=True,
                        help="Path to the Tokenizer")
parser.add_argument("-I", "--input-length", type=int, default=55,
                        help="input token size")
parser.add_argument("-M", "--model", type=str, required=True,
                        help="model name")
parser.add_argument("-P", "--process-num", type=int, default=64,
                        help="process num, default is 64")
parser.add_argument("-O", "--max-tokens", type=int, default=500,
                        help="output length, default is 500")
parser.add_argument("-D", "--dataset", type=str, default="",
                        help="can set this to specify dataset, when set -I/--input_len is useless")

parser.add_argument("--port", type=int, default=8000, help="openai api port, default is 8000")

parser.add_argument("--perf", action="store_true", default=False)
parser.add_argument("--debug", action="store_true", default=False)

if __name__ == "__main__":
    args = parser.parse_args()
    if args.dataset == "":
        os.system(f"python3 gen.py -T {args.tokenizer} -L {args.input_length}")
    else:
        print(f"use dataset: {args.dataset}")
    cmd = f"python3 run_single.py -M {args.model}                           \
                                    -N {args.tokenizer}                     \
                                    -P {args.process_num}                   \
                                    --port {args.port}                      \
                                    -L {args.max_tokens}"   
    # specify dataset
    if args.dataset == "":
        cmd += f" -D data/data_{args.input_length}.json"
    else:
        cmd += f" -D {args.dataset}"                                   
    if args.perf:
        cmd += " --perf"
    if args.debug:
        cmd += " --debug"
    os.system(cmd)
