from transformers import AutoTokenizer, GPT2TokenizerFast
from huggingface_hub import hf_hub_download
from .constants import FILE_DIR, GPT2_MERGE_DIR, GPTJ_MERGE_DIR
import json
import os
from typing import Dict


def merge(thai_tokenizer_repo: str = "flax-community/gpt2-base-thai"):
    # load tokenizer
    gptj_tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-j-6B")
    gpt2_tokenizer = AutoTokenizer.from_pretrained(thai_tokenizer_repo)

    # load vcab and merge rule
    hf_hub_download(
        repo_id="EleutherAI/gpt-j-6b",
        filename="merges.txt",
        local_dir=f"{FILE_DIR}/GPTJ_merge_rule/",
    )
    hf_hub_download(
        repo_id=thai_tokenizer_repo,
        filename="merges.txt",
        local_dir=f"{FILE_DIR}/GPT2_merge_rule/",
    )

    # retrieve the vocabs
    gptj_vocab = gptj_tokenizer.get_vocab()
    gpt2_vocab = gpt2_tokenizer.get_vocab()

    # create folder to keep new vocab and merge
    folder_path = "./temp"
    os.mkdir(folder_path)

    # Create a new vocabulary by merging vocabs
    new_vocab: Dict[str, int] = {}
    idx = 0
    for word in gptj_vocab.keys():
        if word not in new_vocab.keys():
            new_vocab[word] = gptj_vocab[word]
            idx += 1

    # Add words from second tokenizer
    for word in gpt2_vocab.keys():
        if word not in new_vocab.keys():
            new_vocab[word] = idx
            idx += 1

    # convert dictionary to json
    new_vocab_json = json.dumps(new_vocab, ensure_ascii=False)

    # write json to a file
    vocab_file_path = os.path.join(folder_path, "merge_vocab.json")

    with open(vocab_file_path, "w", encoding="utf-8") as outfile:
        outfile.write(new_vocab_json)

    # merge merged rule
    merge_file_path = os.path.join(folder_path, "new_merged_rule.txt")

    with open(GPT2_MERGE_DIR, "r", encoding="utf-8") as f1, open(
        GPTJ_MERGE_DIR, "r", encoding="utf-8"
    ) as f2, open(merge_file_path, "w", encoding="utf-8") as out_file:
        # Ignore first line of each input file
        next(f1)
        next(f2)

        # Read the remaining lines of each file and write them to the output file
        lines = set()
        for line in f1:
            if line not in lines:
                out_file.write(line)
                lines.add(line)
        for line in f2:
            if line not in lines:
                out_file.write(line)
                lines.add(line)

    merge_tokenizer = GPT2TokenizerFast(
        vocab_file=vocab_file_path, merges_file=merge_file_path
    )

    return merge_tokenizer
