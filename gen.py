from transformers import AutoTokenizer
import argparse
import json
parser = argparse.ArgumentParser(
    "generator token size most close to input -L|--length"
)
parser.add_argument("-T", "--tokenizer", type=str, required=True,
                        help="Path to the Tokenizer")
parser.add_argument("-L", "--length", type=int, required=True,
                        help="input token size")
parser.add_argument("-B", "--base", type=str, default="data/base.txt",
                        help="path to the generator base txt")

def get(x):
    l = 1
    r = len(s)
    print(len(s))
    while l < r:
        mid = (int) ((l + r) / 2)
        t = len(tok.encode(s[0:mid]))
        if t == x:
            return mid
        elif t < x:
             l = mid + 1
        else:
             r = mid - 1
    return l

if __name__ == "__main__":
    log = []
    args = parser.parse_args()
    tokenizer = args.tokenizer
    tar = args.length
    tok = AutoTokenizer.from_pretrained(tokenizer)
    f = open(args.base, "r")
    s = f.readline()
    ret = s[0:get(tar)]
    print(f"get len {len(tok.encode(ret))}")
    print(ret)
    file_name = f"data/data_{args.length}.json"
    log.append(
        {
            # "model": model,
            "prompt": ret,
        }
    )
    with open(file_name, "w") as f:
        json.dump(log, f, indent=4, ensure_ascii=False)
    
