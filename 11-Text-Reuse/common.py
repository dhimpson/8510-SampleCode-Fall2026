"""
Shared helpers for this week's scripts.

The scripts work on any corpus in one of two shapes:

  - a folder of .txt files (subfolders are searched too), or
  - a .csv file with a "text" column, and if you like an "id" column.

read_passages() turns either one into a list of passages, each a dictionary
like {"id": "letter_1862-03-01", "text": "My dear sister ..."}.

Passages come back in corpus order: files sorted by name, CSV rows top to
bottom. If you name your files (or sort your CSV) by date, every script's
results come out in time order.
"""

import csv
import re
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
OUTPUT_FOLDER = SCRIPT_DIR / "output"

# Column names to use when the corpus is a CSV file
TEXT_COLUMN = "text"
ID_COLUMN = "id"

# A word is a run of letters, with apostrophes and hyphens allowed inside
# (so numbers and punctuation are not words)
WORD = re.compile(r"[a-z]+(?:['-][a-z]+)*")


def read_passages(corpus, passage_words=0):
    """Every passage in the corpus, in order.

    corpus: a folder of .txt files, or a .csv file with a TEXT_COLUMN.
    passage_words: cut each text into passages of this many words
                   (0 = each file or row is one passage).
    """
    path = SCRIPT_DIR / Path(corpus).expanduser()

    # 1. Read every text with a name (its id)
    texts = []
    if path.is_dir():
        for file in sorted(path.rglob("*.txt")):
            name = str(file.relative_to(path).with_suffix(""))
            texts.append((name, file.read_text(encoding="utf-8", errors="replace")))
    elif path.suffix.lower() == ".csv" and path.exists():
        csv.field_size_limit(2**31 - 1)  # some texts are very long
        with open(path, newline="", encoding="utf-8", errors="replace") as f:
            reader = csv.DictReader(f)
            if TEXT_COLUMN not in (reader.fieldnames or []):
                raise SystemExit(f"{path.name} has no '{TEXT_COLUMN}' column. "
                                 f"Rename yours, or change TEXT_COLUMN in common.py.")
            for row_number, row in enumerate(reader, 1):
                texts.append((row.get(ID_COLUMN) or f"row {row_number}", row[TEXT_COLUMN] or ""))
    else:
        raise SystemExit(f"Can't find {corpus}. CORPUS should be a folder of .txt files or a "
                         f".csv file, next to the scripts or given as a full path.")
    if not texts:
        raise SystemExit(f"No .txt files in {corpus}.")

    # 2. Keep each text whole, or cut it into passages of passage_words words
    if passage_words <= 0:
        return [{"id": name, "text": text} for name, text in texts]
    passages = []
    for name, text in texts:
        words = text.split()
        for start in range(0, len(words), passage_words):
            chunk = words[start:start + passage_words]
            passages.append({"id": f"{name}, words {start + 1}-{start + len(chunk)}",
                             "text": " ".join(chunk)})
    return passages


def phrases(text, n):
    """Every run of n words in the text, as a set (the same idea as 01's word_ngrams)."""
    words = WORD.findall(text.lower())
    starts = range(len(words) - n + 1)
    return {" ".join(words[i:i + n]) for i in starts}


def jaccard(a, b):
    """Shared pieces / all the different pieces (0 if neither has any), as in 01.

    All the different pieces = A's pieces + B's pieces - the shared ones (which
    would otherwise be counted twice). Counting this way, without building a
    new set, is about 15 times faster when you compare thousands of pairs."""
    shared = len(a & b)
    total = len(a) + len(b) - shared
    return shared / total if total else 0.0


def snippet(text, shared, n, length=25):
    """About `length` words of the text, starting at the first phrase in `shared`,
    lowercased and without punctuation (the way the scripts see it)."""
    words = WORD.findall(text.lower())
    for i in range(len(words) - n + 1):
        if " ".join(words[i:i + n]) in shared:
            return " ".join(words[i:i + length])
    return " ".join(words[:length])
