#!/usr/bin/env python3
"""
Compare how the three NER methods handled a few test entities.

For each test entity, show whether spaCy, GLiNER, and Gemini found it,
how many times, and with which label(s). Edit FILES and TESTS to fit.

Prints the comparison and saves it to output/compare_entities.csv

    python compare_entities.py
"""

import csv
import re
from collections import Counter
from pathlib import Path

OUTPUT = Path(__file__).parent / "output"
RESULTS_FILE = OUTPUT / "compare_entities.csv"

# Which CSV holds each method's results (rename to match your files)
FILES = {
    "spaCy":  OUTPUT / "output_NAACP_1933_01_spacy.csv",
    "GLiNER": OUTPUT / "output_NAACP_1933_02_gliner.csv",
    "Gemini": OUTPUT / "output_NAACP_1933_03_gemini.csv",
}

# Test entities: (what to search for, exact match?)
# exact=True  -> the entity text must equal it exactly (good for "I")
# exact=False -> the search text appears anywhere in the entity
TESTS = [
    ("Oxner", False),
    ("White", False),
    ("N. A. C. P.", True),      # the typo on p. 20
    ("Greenville, N. C.", False),
    ("N. C.", True),
    ("I", True),                # the pronoun
    ("Roy Hudson", False),
    ("Luther Hudson", False),
    ("George Green", False),
    ("Library of Congress", False),   # from the transcription header
]


def clean(text):
    """Turn line breaks and runs of spaces into one space."""
    return re.sub(r"\s+", " ", text).strip()


def load(path):
    with open(path, encoding="utf-8") as f:
        return [{**row, "text": clean(row["text"])} for row in csv.DictReader(f)]


def main():
    results = {}
    for method, path in FILES.items():
        if path.exists():
            results[method] = load(path)
            print(f"{method:7} {len(results[method]):4} entities  ({path.name})")
        else:
            print(f"{method:7} MISSING: {path.name} -- fix FILES at the top")
    print()

    rows_out = []   # one row per test entity per method, for the CSV
    for term, exact in TESTS:
        print(f'"{term}"')
        for method, rows in results.items():
            if exact:
                hits = [r for r in rows if r["text"] == term]
            else:
                hits = [r for r in rows if term.lower() in r["text"].lower()]

            labels = Counter(r["label"] for r in hits)
            labels_text = ", ".join(f"{label} x{n}" for label, n in labels.items())
            examples = sorted({r["text"] for r in hits})[:3]

            if hits:
                print(f"   {method:7} {labels_text}   e.g. {examples}")
            else:
                print(f"   {method:7} --")

            rows_out.append({
                "entity": term,
                "method": method,
                "found": "yes" if hits else "no",
                "count": len(hits),
                "labels": labels_text,
                "examples": "; ".join(examples),
            })
        print()

    # Save the comparison as a CSV
    OUTPUT.mkdir(exist_ok=True)
    columns = ["entity", "method", "found", "count", "labels", "examples"]
    with open(RESULTS_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows_out)
    print(f"Saved {RESULTS_FILE.relative_to(Path(__file__).parent)}")


if __name__ == "__main__":
    main()
