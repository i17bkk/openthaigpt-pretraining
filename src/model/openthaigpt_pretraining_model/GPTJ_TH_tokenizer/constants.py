import os

FILE_DIR = os.path.dirname(__file__)

GPT2_MERGE_DIR = f"{FILE_DIR}/GPT2_merge_rule/merges.txt"
GPTJ_MERGE_DIR = f"{FILE_DIR}/GPTJ_merge_rule/merges.txt"
OUTPUT_HF_DIR = f"{FILE_DIR}/merged_GPTJ_tokenizer_hf"
NEW_TOKEN_DIR = f"{FILE_DIR}/merged_GPTJ_tokenizer_hf/tokenizer.json"
