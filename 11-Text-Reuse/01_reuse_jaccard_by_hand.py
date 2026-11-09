#!/usr/bin/env python3
"""
Step 1: N-grams, shingles, and Jaccard similarity
=================================================

Breaks two short texts into overlapping pieces, two ways:

  - word n-grams:       runs of N words       ("honorary members", "members shall", ...)
  - character shingles: runs of K characters  ("honor", "onora", "norar", ...)

then measures how much the two sets of pieces overlap with Jaccard similarity:

    pieces the two texts share / all the different pieces in either text

0 = nothing in common, 1 = the same set of pieces.

Change TEXT_A and TEXT_B (and N, K, CLEAN) and run it again.
"""

import re

# --- Change these --------------------------------------------------------------

# One clause of the American Physical Education Association's constitution, as
# adopted in 1886 and in 1895 (both reprinted in test/APER_1909_November.txt)
TEXT_A = ("Honorary members shall not exceed the proportion of one to twenty-five active "
          "members, and shall consist of persons well known as patrons of physical education. "
          "They shall be nominated by the Council — and require a two-thirds vote of the "
          "members present to elect.")
TEXT_B = ("Honorary Members shall not exceed the proportion of one to twenty-five Active "
          "Members, and shall consist of persons well known as patrons of physical education. "
          "They shall be nominated by the Executive Committee and require a two-thirds vote "
          "of the members present to elect.")

N = 2           # words per n-gram
K = 5           # characters per shingle
CLEAN = True    # lowercase and drop punctuation before comparing?

# -------------------------------------------------------------------------------


def clean(text):
    """Lowercase, drop punctuation (both kinds of apostrophe included),
    and squeeze runs of spaces down to one."""
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    return " ".join(text.split())


def word_ngrams(text, n):
    """Every run of n words, as a set."""
    words = text.split()
    starts = range(len(words) - n + 1)
    return {" ".join(words[i:i + n]) for i in starts}


def char_shingles(text, k):
    """Every run of k characters (spaces included), as a set."""
    return {text[i:i + k] for i in range(len(text) - k + 1)}


def jaccard(a, b):
    """Shared pieces / all the different pieces.
    If neither text has any pieces (say, word pairs from two one-word names),
    there's nothing to compare, so the score is 0, not a match."""
    if not a | b:
        return 0.0
    return len(a & b) / len(a | b)


def show(label, a, b):
    shared, everything = a & b, a | b
    print(f"\n{label}")
    print(f"  A ({len(a)}): {sorted(a)}")
    print(f"  B ({len(b)}): {sorted(b)}")
    print(f"  shared ({len(shared)}): {sorted(shared)}")
    print(f"  Jaccard = {len(shared)} shared / {len(everything)} total = {jaccard(a, b):.2f}")


def main():
    a, b = (clean(TEXT_A), clean(TEXT_B)) if CLEAN else (TEXT_A, TEXT_B)
    print(f"A: {a!r}")
    print(f"B: {b!r}")

    show(f"Word {N}-grams", word_ngrams(a, N), word_ngrams(b, N))
    show(f"Character {K}-shingles", char_shingles(a, K), char_shingles(b, K))


if __name__ == "__main__":
    main()
