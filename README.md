![image](https://raw.githubusercontent.com/Shishir-Kc/Assets/main/Ember/screenshot-2026-09-16_09-56-06.png)
# Ember

Ember is a custom Byte-Pair Encoding (BPE) tokenizer, the first release in an ongoing tokenizer family (Ember, Flare, Nova, Supernova) built to serve as the tokenization layer for future language models in this project.

## Overview

Tokenization is the first transformation any language model applies to raw text, and the quality of that transformation sets a ceiling on everything downstream: sequence length, training efficiency, and how well the model generalizes across vocabulary it has never seen in exactly that form. Ember was built to give this project a tokenizer trained from scratch on its own data, rather than relying on a general purpose off the shelf vocabulary.

## Why Ember

Most publicly available tokenizers (GPT-2, GPT-4, LLaMA, etc.) are trained on large, broad, English dominant web corpora. That works well for general purpose models, but it is not necessarily the right fit for a purpose built model trained on a specific corpus. Ember exists to:

- Give full control over vocabulary composition, size, and merge behavior
- Establish a baseline BPE implementation that later tokenizers in the family can be benchmarked against
- Build the internal tooling and training pipeline needed to iterate on tokenizer design going forward

## How It Works

Ember uses standard Byte-Pair Encoding: it starts from individual bytes/characters, and iteratively merges the most frequent adjacent pair of tokens into a new token, repeating until the target vocabulary size is reached. Each merge is learned directly from the training corpus, so the resulting vocabulary reflects the actual statistical structure of that text.

## Training Details

| Property | Value |
|---|---|
| Algorithm | Byte-Pair Encoding (BPE) |
| Corpus size | 1 GB text |
| Vocabulary size | 40,000 |
| Implementation | Pure Python |

## Limitations and Known Problems

Ember's first release comes with a few known limitations, mostly inherited from standard BPE itself:

- **Greedy, deterministic merges.** BPE always merges the single most frequent pair at each step, with no mechanism to reconsider earlier merges once made. This can lock in suboptimal splits for rarer words.
- **Single tokenization path.** Ember produces exactly one tokenization per input string, with no built in subword regularization or sampling, which some training setups use to improve robustness.
- **Corpus dependent bias.** Because the vocabulary is learned entirely from the training corpus, tokenization quality on text that looks very different from that corpus (different language, domain, or formatting) will be weaker.
- **Pure Python implementation.** The current training pipeline is not optimized for speed, which limits how quickly larger corpora or vocabularies can be trained.
- **No formal compression benchmarking yet.** Ember has not yet been evaluated against standard tokenizer quality metrics (compression ratio, tokens per word, out of vocabulary rate) relative to established tokenizers.

## Planned Solutions and Roadmap

These limitations are directly driving the design of the next tokenizer in the family:

- A new merge/segmentation algorithm that is not just a faster version of BPE, but a genuinely different rule, aimed at improving training speed, encoding speed, and compression ratio together rather than trading one off against the others
- A larger target vocabulary, roughly 2 to 4 times the size of Ember's
- A training corpus that spans multiple languages rather than a single one
- A training loop reimplemented in Rust for performance, once the algorithm itself is validated in Python
- Proper baseline metrics and evaluation, so future tokenizers in the family can be compared against Ember and each other on equal footing

## Tokenizer Family

Ember is the first entry in a planned lineage:

```
Ember -> Flare -> Nova -> Supernova
```

Each successor is intended to build on the lessons learned from the one before it.



