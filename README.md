# VLLM Test

### Setup

```shell
./init
```
### usage

```shell
usage: python3 main.py [-h] -T TOKENIZER [-I INPUT_LENGTH] -M MODEL [-P PROCESS_NUM] [-O MAX_TOKENS] [-D DATASET] [--port PORT] [--perf] [--debug]

options:
  -h, --help            show this help message and exit
  -T TOKENIZER, --tokenizer TOKENIZER
                        Path to the Tokenizer
  -I INPUT_LENGTH, --input-length INPUT_LENGTH
                        input token size
  -M MODEL, --model MODEL
                        model name
  -P PROCESS_NUM, --process-num PROCESS_NUM
                        process num, default is 64
  -O MAX_TOKENS, --max-tokens MAX_TOKENS
                        output length, default is 500
  -D DATASET, --dataset DATASET
                        can set this to specify dataset, when set -I/--input_len is useless
  --port PORT           openai api port, default is 8000
  --perf                whether analysize performence
  --debug               whether print debug log
```

### example

```shell
python main.py -T /workspace/models/Llama-2-7b-hf/ -M /workspace/models/Llama-2-7b-hf/ -O 500 -P 64  --perf --debug -I 55

# use specify data and port
python main.py -T /workspace/models/Llama-2-7b-hf/ -M /workspace/models/Llama-2-7b-hf/ -O 500 -P 64  --perf --debug -I 55 --port 8001 -D data/data.json
```