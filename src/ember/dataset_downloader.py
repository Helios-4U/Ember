from datasets import load_dataset

ds = load_dataset("wikimedia/wikipedia", "20231101.en", split="train", streaming=True)

text = []
size = 0
target = 500_000_000  # 500MB in bytes

for row in ds:
    t = row["text"]
    text.append(t)
    size += len(t.encode("utf-8"))
    if size >= target:
        break

with open("wiki_500mb.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(text))
