# VLLM Test

### Setup

```shell
./init
```


### usage

```shell
# run.py
usage: run.py [-h] -D DATASET [--perf]

run [min_pool_size, max_pool_size] [min_output, max_output]

options:
  -h, --help            show this help message and exit
  -D DATASET, --dataset DATASET
                        Path to the dataset. notes:if path is .*_<num>.json, then can recognise input len as <num>
  --perf

# run_single.py
request dataset by defined pool size and max tokens

options:
  -h, --help            show this help message and exit
  -D DATASET, --dataset DATASET
                        Path to the dataset.
  -P PROCESS_NUM, --process-num PROCESS_NUM
                        process num, default is 64
  -L MAX_TOKENS, --max-tokens MAX_TOKENS
                        output length, default is 500
  -B, --debug           print debug log
  -T TEMPERATURE, --temperature TEMPERATURE
                        random magic number, default is 0 mean there is no random
  --perf

# gen.py
usage: generator token size most close to input -L|--length [-h] -M MODEL -L LENGTH [-B BASE]

options:
  -h, --help            show this help message and exit
  -M MODEL, --model MODEL
                        Path to the model.
  -L LENGTH, --length LENGTH
                        output token size
  -B BASE, --base BASE  path to the generator base txt

#trivial_gen.py 
usage: trivial_gen.py [-h] -L LEN -M MODEL

generator input data with specified length but string may meaningless

options:
  -h, --help            show this help message and exit
  -L LEN, --len LEN     input token size
  -M MODEL, --model MODEL
                        model name
```

### example

```shell
python gen.py -M /workspace/models/Llama-2-7b-hf/ -L 55

python run_single.py -D data/data_55.json 
```