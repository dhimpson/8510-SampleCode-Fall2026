#!/usr/bin/env python3
"""
Step 2: Compare every passage with every other passage
======================================================

The same three moves as 01 (chop, compare, score), on a whole corpus:

  1. Read the corpus and cut it into passages.
  2. Chop every passage into N-word phrases.
  3. Compare every passage with every other one, and score each pair (Jaccard).
  4. Keep the pairs that score at least MATCH, best first.

Point CORPUS at your own texts: a folder of .txt files, or a .csv file with a
"text" column (see common.py). The default is the test folder: two issues of
the American Physical Education Review (November 1909, December 1910). Issues
are long, so PASSAGE_WORDS cuts them into short passages first.

Every pair gets compared, so the work grows fast. 1,000 passages make about
500,000 pairs (a second or two); 10,000 make 50 million (a minute or two);
100,000 make 5 billion (hours). For a corpus that big, see 03_reuse_minhash.py.

Results are saved to output/02_pairs.csv.
"""

import csv

from common import OUTPUT_FOLDER, SCRIPT_DIR, jaccard, phrases, read_passages, snippet

# --- Change these --------------------------------------------------------------

CORPUS = "test"    # a folder of .txt files, or a .csv file with a "text" column
PASSAGE_WORDS = 75       # cut long texts into passages of this many words (0 = keep whole)
N = 5                   # words per phrase
MATCH = 0.5             # keep pairs that share at least this share of their phrases
SHOW = 10               # pairs to print

# -------------------------------------------------------------------------------


def main():
    # 1. Read the corpus
    passages = read_passages(CORPUS, PASSAGE_WORDS)
    total = len(passages) * (len(passages) - 1) // 2
    print(f"{len(passages):,} passages, so {total:,} pairs to compare...")

    # 2. Chop every passage into phrases (once, before comparing)
    pieces = [phrases(p["text"], N) for p in passages]

    # 3. Compare every passage with every other one.
    #    j starts after i, so each pair is compared once.
    pairs = []
    for i in range(len(passages)):
        for j in range(i + 1, len(passages)):
            score = jaccard(pieces[i], pieces[j])
            if score >= MATCH:
                pairs.append((score, i, j))

    # 4. Best first (ties stay in corpus order)
    pairs.sort(key=lambda pair: pair[0], reverse=True)

    print(f"{len(pairs):,} pairs share at least {MATCH:.0%} of their phrases.\n")
    for score, i, j in pairs[:SHOW]:
        print(f"{score:.2f}  {passages[i]['id']}")
        print(f"      {passages[j]['id']}")
        print(f"      \"{snippet(passages[i]['text'], pieces[i] & pieces[j], N)} ...\"\n")

    OUTPUT_FOLDER.mkdir(exist_ok=True)
    path = OUTPUT_FOLDER / "02_pairs.csv"
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["score", "passage_a", "passage_b", "text_a", "text_b"])
        for score, i, j in pairs:
            writer.writerow([round(score, 2), passages[i]["id"], passages[j]["id"],
                             passages[i]["text"], passages[j]["text"]])
    print(f"Saved {path.relative_to(SCRIPT_DIR)}")


if __name__ == "__main__":
    main()
