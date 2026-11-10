#!/usr/bin/env python3
"""
Step 4: How did one clause change over time?
============================================

Finds every sentence in the corpus that contains most of the words of START (a
few words from the clause you want to follow), and compares each version with
the one before it: how similar they are, and which words were added or cut.

A sentence only needs SHARE of START's 3-word phrases, so small differences
don't knock it out. Each version shows the matching sentence plus the next one.
A long text, like a whole issue of a journal, can hold more than one version.

Versions appear in corpus order (files sorted by name, CSV rows top to bottom),
so name or sort your texts by date to see change over time.

The page (output/04_trace.html) shows every version, with the changes from the
version before highlighted, and opens in your browser.
"""

import difflib
import html
import re
import webbrowser

from common import OUTPUT_FOLDER, SCRIPT_DIR, jaccard, phrases, read_passages

# --- Change these --------------------------------------------------------------

CORPUS = "test"         # a folder of .txt files, or a .csv file with a "text" column
START = "honorary members shall not exceed the proportion of one to twenty-five"
SHARE = 0.6             # share of START's 3-word phrases a sentence must contain
SENTENCES = 2           # how many sentences to show, starting with the match

OPEN_IN_BROWSER = True

# -------------------------------------------------------------------------------

TOKEN = re.compile(r"\S+")


def versions(text, target):
    """Every sentence in the text with at least SHARE of START's phrases, plus
    the sentences after it, as (sentence number, excerpt) pairs."""
    text = " ".join(text.split())  # line breaks and runs of spaces become one space
    sentences = re.split(r"(?<=[.:;])\s+", text)
    found = []
    for k, sentence in enumerate(sentences):
        if len(target & phrases(sentence, 3)) / len(target) >= SHARE:
            found.append((k + 1, " ".join(sentences[k:k + SENTENCES])))
    return found


def changes(old, new):
    """The new text as HTML: words added since the old version in green,
    words cut from it in red (struck through)."""
    a, b = TOKEN.findall(old), TOKEN.findall(new)
    out = []
    matcher = difflib.SequenceMatcher(None, [w.lower() for w in a], [w.lower() for w in b],
                                      autojunk=False)
    for op, i1, i2, j1, j2 in matcher.get_opcodes():
        if op == "equal":
            out.append(html.escape(" ".join(b[j1:j2])))
            continue
        if i2 > i1:
            out.append(f'<del>{html.escape(" ".join(a[i1:i2]))}</del>')
        if j2 > j1:
            out.append(f'<ins>{html.escape(" ".join(b[j1:j2]))}</ins>')
    return " ".join(out)


def main():
    passages = read_passages(CORPUS)
    target = phrases(START, 3)
    if not target:
        raise SystemExit("START needs at least three words.")
    found = []
    for p in passages:
        # Skip texts that don't have enough of START anywhere (quick check)
        if len(target & phrases(p["text"], 3)) / len(target) < SHARE:
            continue
        for number, text in versions(p["text"], target):
            found.append((f"{p['id']}, sentence {number}", text))
    if not found:
        print("No versions found. Try a lower SHARE or different words in START.")
        return

    print(f"\"{START}\": {len(found)} versions\n")
    parts, previous = [], None
    for where, text in found:
        if previous is None:
            similarity, body = "", html.escape(text)
            print(f"  {where[:40]:40s}       {text[:80]}")
        else:
            score = jaccard(phrases(previous, 3), phrases(text, 3))
            similarity = f"3-gram Jaccard with the version before: {score:.2f}"
            body = changes(previous, text)
            print(f"  {where[:40]:40s} {score:.2f}  {text[:80]}")
        parts.append(f"<h2>{html.escape(where)}</h2>"
                     f"<p class='score'>{similarity}</p><p>{body}</p>")
        previous = text

    page = f"""<!doctype html><html><head><meta charset="utf-8"><title>{html.escape(START)}</title>
<style>
 body {{ font-family: Georgia, serif; max-width: 900px; margin: 2em auto; padding: 0 1em;
        line-height: 1.6; color: #141d2e; }}
 h1, h2, .score {{ font-family: Helvetica, Arial, sans-serif; }}
 h2 {{ margin-top: 2em; border-top: 1px solid #ddd; padding-top: 1em; font-size: 1.1em; }}
 .score {{ color: #555; font-size: 0.9em; }}
 ins {{ background: #c6f6d5; text-decoration: none; }}
 del {{ background: #fed7d7; }}
</style></head><body>
<h1>“{html.escape(START)}”</h1>
<p>{len(found)} versions, in corpus order. <ins>Green</ins>: added since the version before.
<del>Red</del>: cut since the version before.</p>
{''.join(parts)}
</body></html>"""
    OUTPUT_FOLDER.mkdir(exist_ok=True)
    path = OUTPUT_FOLDER / "04_trace.html"
    path.write_text(page, encoding="utf-8")
    print(f"\nSaved {path.relative_to(SCRIPT_DIR)}")
    if OPEN_IN_BROWSER:
        webbrowser.open(path.resolve().as_uri())


if __name__ == "__main__":
    main()
