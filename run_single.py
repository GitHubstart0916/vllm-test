import time
from multiprocessing import Pool
from multiprocessing import Process
from multiprocessing import Manager
from transformers import AutoTokenizer
import openai
from openai import OpenAI
import time
import numpy as np
from typing import AsyncGenerator, List, Tuple
import json
import argparse

# prompt_len output_len, latency
REQUEST_LATENCY: List[Tuple[int, int, float]] = []
parser = argparse.ArgumentParser(
        description="request dataset by defined pool size and max tokens")
parser.add_argument("-D", "--dataset", type=str, required=True,
                        help="Path to the dataset.")
parser.add_argument("-M", "--model", type=str, required=True,
                        help="model name")
parser.add_argument("-P", "--process-num", type=int, default=64,
                        help="process num, default is 64")
parser.add_argument("-L", "--max-tokens", type=int, default=500,
                        help="output length, default is 500")
parser.add_argument("-B", "--debug", action="store_true", default=False, 
                        help="print debug log")
parser.add_argument("-T", "--temperature", type=float, default=0.0,
                        help="random magic number, default is 0 mean there is no random")

parser.add_argument("--perf", action="store_true", default=False)

openai_api_key = "EMPTY"
openai_api_base = "http://localhost:8000/v1"
def bench_openai(ret_list, perf_list, model, prompt):
    client_t = OpenAI(
        api_key=openai_api_key,
        base_url=openai_api_base,)
    send_request(client_t, ret_list, perf_list, model, prompt)

def send_request(client, ret_list, perf_list, model, prompt, echo=False, stream=False, gene_num=1, logprobs=3):
    # print("send")
    start_ns = time.perf_counter_ns()
    completion = client.completions.create(
        model=model,
        prompt=prompt,
        echo=echo,
        n=gene_num,
        stream=stream,
        logprobs=logprobs,
        temperature=args.temperature,
        max_tokens=args.max_tokens)
    end_ns = time.perf_counter_ns()
    tokens = completion.usage.completion_tokens
    # if args.debug:
    #     print(completion.choices[0].text)
    ret_list.append(completion.choices[0].text)
    perf_list.append((tokens, (end_ns - start_ns)/1000.0/1000.0))
    # print(completion.usage.prompt_tokens, tokens, (end_ns - start_ns)/1000.0/1000.0)


if __name__ == "__main__":
    manager = Manager()
    ret_list = manager.list()
    perf_list = manager.list()
    args = parser.parse_args()
    pool_size = args.process_num
    
    print(f"run on args: {args}")
    model = args.model
    with open(args.dataset) as f:
        dataset = json.load(f)
        for data in dataset:
            # model = data["model"]
            prompt = data["prompt"]
            # send_request(model=model, prompt=prompt)
        tok = AutoTokenizer.from_pretrained(model)
        with Pool(pool_size) as p:
            p_args = [(ret_list, perf_list, model, prompt) for _ in range(pool_size)]
            # print(len(args))
            results = p.starmap(bench_openai, p_args)
            p.close()
            p.join()
            statu = "Accept"
            if args.temperature == 0.0:
                for t in ret_list:
                    if t != ret_list[0]:
                        statu = "return token different from each other"
            # print(tok.encode(ret_list[0]))
            ave_time = 0.0
            ave_token_per_sec = 0.0
            for a, b in perf_list:
                ave_time += b
                ave_token_per_sec += a / (b / 1000.0)
            ave_time /= pool_size
            ave_token_per_sec /= pool_size
            tokens = tok.encode(ret_list[0])
            input_len = len(tok.encode(prompt))
            output_len = perf_list[0][0]
            if not args.perf:
                log = {
                    "input_len": input_len,
                    "max_tokens": output_len,
                    "recive_tokens_len": len(tokens),
                    "thread_num": pool_size,
                    "statu": statu,
                    "output_tokens": tokens
                }
            else:
                log = {
                    "input_len": input_len,
                    "max_tokens": output_len,
                    "recive_tokens_len": len(tokens),
                    "thread_num": pool_size,
                    "statu": statu,
                    "output_tokens": tokens,
                    "average_latency": ave_time,
                    "token_per_sec": ave_token_per_sec
                }
            with open(f"log/in_{input_len}_out_{output_len}_process_{pool_size}.json", "w") as f:
                json.dump(log, f, indent=4, ensure_ascii=False)
            print(statu + f" and log in log/in_{input_len}_out_{output_len}_process_{pool_size}.json")
            if args.perf:
                print(f"average_latency: {ave_time}\ntoken_per_sec: {ave_token_per_sec}")
            # print(out_tokens)
            # print(len(tok.encode(ret_list[0])))


