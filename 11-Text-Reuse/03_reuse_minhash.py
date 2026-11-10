#!/usr/bin/env python3
"""
Step 3 (optional): The same comparison, fast enough for a big corpus
====================================================================

You only need this if 02 is too slow. 02 compares every pair of passages, so
the work grows with the square of the corpus: 100,000 passages make 5 billion
pairs, hours of work. This script finds nearly the same pairs without comparing
them all, with the shortcut Kellen Funk and Lincoln Mullen used in "The Spine
of American Law" (2018), and their settings: MinHash and locality-sensitive
hashing (LSH).

  1. Chop every passage into N-word phrases and turn each phrase into a number.
  2. Boilerplate: ignore any phrase found in more than MAX_PASSAGES passages
     (mastheads, headers, legal formulas that appear everywhere).
  3. MinHash: give every passage a signature of HASHES numbers. Each of HASHES
     scrambling formulas gives every phrase a new number; the passage keeps the
     smallest. The share of signature numbers two passages have in common
     estimates their Jaccard score.
  4. LSH: cut each signature into BANDS bands. Passages that match on a whole
     band land in the same bucket. Only passages in the same bucket get compared.
  5. Group: link every pair that scores at least MATCH, directly or through a
     chain, into groups of passages that share language. Print the biggest.

Point CORPUS at your own texts, as in 02. Run 02 and 03 on the same corpus and
compare output/02_pairs.csv with output/03_pairs.csv: they should mostly agree,
with 03's scores (estimates) a few hundredths off.

Saves output/03_pairs.csv and output/03_groups.csv. On 300,000 passages it
takes about a minute and 1 GB of memory.
"""

import csv
import re
import zlib
from collections import defaultdict

import numpy as np

from common import OUTPUT_FOLDER, SCRIPT_DIR, phrases, read_passages, snippet

# --- Change these --------------------------------------------------------------

CORPUS = "test"         # a folder of .txt files, or a .csv file with a "text" column
PASSAGE_WORDS = 75      # cut long texts into passages of this many words (0 = keep whole)
N = 5                   # words per phrase
MATCH = 0.5             # a match shares at least this share of its phrases (Jaccard)
MAX_PASSAGES = 300      # phrases in more passages than this are boilerplate
                        # (300 suited a corpus of 300,000 passages; set it for yours)
LOOK_FOR = None         # also list the groups with these words: a regex, such as
                        # r"\bconstitution\b" (case doesn't matter), or None to skip
TOP_N = 10              # groups to print in each list
HASHES = 120            # numbers in each signature
BANDS = 60              # bands per signature (HASHES / BANDS numbers per band)

# -------------------------------------------------------------------------------

MIN_PHRASES = 10        # passages with fewer distinctive phrases get no signature
ROWS = HASHES // BANDS
PRIME = 4294967291      # the largest prime below 2**32

# HASHES scrambling formulas of the form (a * x + b) % PRIME, with random a and b.
# (623 is the seed Funk and Mullen used in R; Python's random numbers differ.)
rng = np.random.default_rng(623)
A = rng.integers(1, 2**31, size=(HASHES, 1), dtype=np.uint64)
B = rng.integers(0, 2**32, size=(HASHES, 1), dtype=np.uint64)


def minhash(numbers):
    """A passage's signature: for each formula, the smallest scrambled phrase number."""
    x = numbers.astype(np.uint64)
    return ((A * x + B) % PRIME).min(axis=1)


def main():
    print("Reading the corpus...")
    passages = read_passages(CORPUS, PASSAGE_WORDS)

    print(f"1. Chopping {len(passages):,} passages into {N}-word phrases...")
    # crc32 is a quick, standard way to turn text into a number
    numbered = []
    for p in passages:
        phrase_set = phrases(p["text"], N)
        numbers = [zlib.crc32(x.encode()) for x in phrase_set]
        numbered.append(np.array(numbers, dtype=np.uint32))

    print(f"2. Boilerplate: phrases found in more than {MAX_PASSAGES} passages...")
    values, counts = np.unique(np.concatenate(numbered), return_counts=True)
    boilerplate = set(values[counts > MAX_PASSAGES].tolist())
    print(f"   {len(boilerplate):,} phrases ignored")

    print("3. MinHash: a signature for every passage...")
    signatures = np.zeros((len(passages), HASHES), dtype=np.uint32)
    usable = []
    for i, numbers in enumerate(numbered):
        distinctive = [x for x in numbers.tolist() if x not in boilerplate]
        if len(distinctive) >= MIN_PHRASES:
            signatures[i] = minhash(np.array(distinctive))
            usable.append(i)
    print(f"   {len(passages) - len(usable):,} passages have fewer than {MIN_PHRASES} "
          f"distinctive phrases and sit out")

    print(f"4. LSH: {BANDS} bands, comparing the passages in each bucket...")
    pairs = {}
    for band in range(BANDS):
        columns = signatures[:, band * ROWS:(band + 1) * ROWS]
        buckets = defaultdict(list)
        for i in usable:
            buckets[columns[i].tobytes()].append(i)
        for members in buckets.values():
            if len(members) < 2:
                continue
            m = np.array(members)
            sig = signatures[m]
            # A table with a row and a column for each passage in the bucket:
            # the share of signature numbers they have in common (≈ Jaccard)
            score = (sig[:, None, :] == sig[None, :, :]).mean(axis=2)
            # Each pair once (row before column), if it scores at least MATCH
            for r, c in zip(*np.nonzero(np.triu(score >= MATCH, k=1))):
                pairs[(int(m[r]), int(m[c]))] = float(score[r, c])

    print("5. Grouping the matches...")
    # Every passage starts as the leader of its own group. Each matching pair
    # merges two groups, and the earlier passage leads the merged group.
    leader = list(range(len(passages)))

    def find(i):
        """Follow the pointers from passage i to its group's leader."""
        while leader[i] != i:
            leader[i] = leader[leader[i]]  # a shortcut for next time
            i = leader[i]
        return i

    for i, j in pairs:
        a, b = find(i), find(j)
        leader[max(a, b)] = min(a, b)
    groups = defaultdict(list)
    for i in sorted({k for pair in pairs for k in pair}):
        groups[find(i)].append(i)

    print(f"\n{len(pairs):,} pairs share at least {MATCH:.0%} of their phrases. "
          f"They make {len(groups):,} groups, holding {sum(map(len, groups.values())):,} "
          f"of {len(passages):,} passages.")

    ranked = sorted(groups, key=lambda g: -len(groups[g]))
    rank = {g: r for r, g in enumerate(ranked, 1)}
    lists = [("Biggest groups", ranked)]
    if LOOK_FOR:
        look_for = re.compile(LOOK_FOR, re.IGNORECASE)
        lists.append(("Biggest groups with LOOK_FOR words (numbered by rank in the list above)",
                      [g for g in ranked if any(look_for.search(passages[k]["text"])
                                                for k in groups[g])]))

    for heading, leaders in lists:
        print(f"\n{heading}:\n")
        for g in leaders[:TOP_N]:
            members = groups[g]
            first, second = members[0], members[1]
            shared = phrases(passages[first]["text"], N) & phrases(passages[second]["text"], N)
            print(f"{rank[g]:5d}. {len(members)} passages")
            print(f"       first: {passages[first]['id']}")
            print(f"       last:  {passages[members[-1]]['id']}")
            print(f"       \"{snippet(passages[first]['text'], shared, N)} ...\"\n")

    OUTPUT_FOLDER.mkdir(exist_ok=True)
    path = OUTPUT_FOLDER / "03_pairs.csv"
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["score", "passage_a", "passage_b"])
        for (i, j), score in sorted(pairs.items(), key=lambda item: -item[1]):
            writer.writerow([round(score, 2), passages[i]["id"], passages[j]["id"]])
    print(f"Saved {path.relative_to(SCRIPT_DIR)}")

    path = OUTPUT_FOLDER / "03_groups.csv"
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["group", "size", "passage", "text"])
        for g in ranked:
            for k in groups[g]:
                writer.writerow([rank[g], len(groups[g]), passages[k]["id"], passages[k]["text"]])
    print(f"Saved {path.relative_to(SCRIPT_DIR)}")
    print("Follow one clause through time with 04_reuse_trace_clause.py.")


if __name__ == "__main__":
    main()
