import os
import argparse
import json
from transformers import AutoTokenizer
min_pool_size = 4
max_pool_size = 12
pool_step = 4

min_output_len = 500
max_ouput_len = 500
output_len_step = 50

parser = argparse.ArgumentParser(
        description="run [min_pool_size, max_pool_size] [min_output, max_output]")
parser.add_argument("-D", "--dataset", type=str, required=True,
                        help="Path to the dataset.\n"
                        + "notes:if path is .*_<num>.json, then can recognise input len as <num>")
# parser.add_argument("-P", "--process-num", type=int, default=-1,
#                         help="process num, default is 64")
# parser.add_argument("-L", "--max-tokens", type=int, default=-1,
#                         help="output length, default is 500")
parser.add_argument("--perf", action="store_true", default=False)

# def analysis(file_name):
#     log = open(file_name)
#     ave_time = 0
#     ave_token_per_sec = 0
#     output_tokens = ""
#     statu = ""
#     num = 0
#     while True:
#         l = log.readline()
#         if not l:
#             break
#         if not l[0].isdigit():
#             if l[0] == "[":
#                 output_tokens = l
#             else:
#                 statu = l[:-1]
#             continue
#         ave_time += float(l.split()[1])
#         ave_token_per_sec += float(l.split()[0]) / (float(l.split()[1]) / 1000.0)
#         num += 1
#         # if num != pool_size:
#         #     exit(-1)
#     return output_tokens, statu, ave_time, ave_token_per_sec

if __name__ == "__main__":
    # run_log = open("log/run_log.csv", "w")
    log = []
    args = parser.parse_args()
    with open(args.dataset) as f:
        dataset = json.load(f)
        for data in dataset:
            model = data["model"]
            prompt = data["prompt"]
    tok = AutoTokenizer.from_pretrained(model)   
    input_len = len(tok.encode(prompt)) 
    # run_log.write("input_size,output_size,process_num,average_latency,token_per_sec\n")
    for pool_size in range(min_pool_size, 
                            max_pool_size + pool_step, 
                            pool_step):
        for output_len in range(min_output_len, 
                                    max_ouput_len + output_len_step, 
                                    output_len_step):
            # print(pool_size, output_len)
            log_name = f"in_{input_len}_out_{output_len}_process_{pool_size}.json"
            os.system(f"python run_single.py -D {args.dataset} -P {pool_size} -L {output_len}")
            # output_tokens, statu, ave_time, ave_token_per_sec = analysis("log/" + log_name)
            with open(f"log/{log_name}") as f:
                single_log = json.load(f)
                log.append(single_log)

    with open("log/run_log.json", "w") as f:
        json.dump(log, f, indent=4, ensure_ascii=False)
    
    print("finish all test!! log in log/run_log.json")
            