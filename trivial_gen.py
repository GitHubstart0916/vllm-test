import argparse
import json
base = "A robot may not injure a human being"
parser = argparse.ArgumentParser(
        description="generator input data with specified length but string may meaningless")
parser.add_argument("-L", "--len", type=int, required=True,
                        help="input token size")
parser.add_argument("-M", "--model", type=str, required=True,
                        help="model name")
if __name__ == "__main__":
    arg = parser.parse_args()
    if arg.len < 10:
        print("len must be large than 10")
    file_name = f"data_{arg.len}.json"
    batch = (int) (arg.len / 10) - 1
    append = arg.len % 10
    for i in range(batch):
        base += ",  robot may not injure a human being"
    for i in range(append):
        base += " A"
    # print(base)
    ret_dict = {"model": arg.model, "prompt": base}
    ret = [ret_dict]
    with open("data/" + file_name, "w") as f:
        json.dump(ret, f, indent=4, ensure_ascii=False)