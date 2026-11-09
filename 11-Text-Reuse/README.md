# Text Reuse

Find passages that one text shares with another, even when the copy isn't exact. Every script
here makes the same three moves:

1. **Chop** each text into short, overlapping pieces (runs of words or letters).
2. **Compare** two texts' pieces and count the ones they share.
3. **Score** the overlap: shared pieces ÷ all the different pieces (Jaccard similarity, 0 to 1).

The scripts work on **any corpus**: point them at your own texts.

| Script | What it does | What you change |
|---|---|---|
| `01_reuse_jaccard_by_hand.py` | N-grams, shingles and Jaccard for two versions of one clause, step by step | `TEXT_A`, `TEXT_B`, `N`, `K`, `CLEAN` |
| `02_reuse_all_pairs.py` | Compares every passage in a corpus with every other one. **This is the main script.** | `CORPUS`, `PASSAGE_WORDS`, `MATCH` |
| `03_reuse_minhash.py` | *If you need it.* Nearly the same answer as 02, fast enough for hundreds of thousands of passages | `CORPUS`, `PASSAGE_WORDS`, `MATCH`, `MAX_PASSAGES` |
| `04_reuse_trace_clause.py` | *If you need it.* Follows one clause through the corpus and shows what changed | `CORPUS`, `START`, `SHARE` |
| `common.py` | Reads any corpus into passages, plus the shared helpers | `TEXT_COLUMN`, `ID_COLUMN` |

---

## Using your own corpus

Set `CORPUS` at the top of 02, 03 or 04 to either:

- **a folder of `.txt` files** (subfolders are searched too). Each file's name becomes its id.
  OCR output from Unit 2 is usually already in this shape.
- **a `.csv` file** with a `text` column, and if you like an `id` column. Your Week 8 extraction
  output works if you name the columns that way (or change `TEXT_COLUMN` and `ID_COLUMN` in `common.py`).

A name on its own (`"my_texts"`) means a folder next to the scripts. A full path works too.

Two more things to decide:

- **What is a passage?** Reuse usually happens at the scale of a paragraph or a clause, not a whole
  document. Two whole journal issues can share a page of text and still score close to 0, because
  that page is a tiny share of everything in them. If your files are long (pages, issues, books), set
  `PASSAGE_WORDS` (try 75 or 100) to cut each one into passages of that many words. `0` keeps each
  file or row whole.
- **Order.** Results come out in corpus order: files sorted by name, CSV rows top to bottom. Start
  your file names with a date (`1909-11_aper.txt`) or sort your CSV by date, and everything comes out
  in time order.

02 compares every pair, so time grows with the square of the corpus: 1,000 passages make about
500,000 pairs (a second or two), 10,000 make 50 million (a minute or two), 100,000 make 5 billion
(hours). Most class corpora are fine with 02. Beyond that, use 03.

---

## The test corpus

The `test` folder holds two issues of the *American Physical Education Review* (November 1909 and
December 1910) as OCR text, about 46,000 words. The November issue's history of the association
reprints all four of its constitutions (1886, 1895, 1903 and 1907), so there is reuse to find. 01's
example comes from it: the honorary-members clause as adopted in 1886 and in 1895.

With `PASSAGE_WORDS = 75`:

- 02 cuts the issues into 616 passages, compares 189,420 pairs in under a second, and finds 8 pairs
  at 0.5 or above. Seven pair the 1903 constitution with the 1907 one. The top pair is two articles
  of the 1903 constitution that say nearly the same thing.
- 03 finds 8 pairs too, 7 of them the same as 02's.
- 04 follows "honorary members shall not exceed the proportion of one to twenty-five" and finds both
  versions of 01's clause: honorary members are nominated by the *Council* in 1886 and by the
  *Executive Committee* in 1895.

Nothing matches *between* the two issues. They share only 21 five-word phrases: the journal's own
name and stock phrases like "it will be seen that".

---

## The method behind 03

03 follows Kellen Funk and Lincoln Mullen, "The Spine of American Law: Digital Text Analysis and
U.S. Legal Practice," *American Historical Review* 123, no. 1 (2018): 132–164,
[doi:10.1093/ahr/123.1.132](https://doi.org/10.1093/ahr/123.1.132). Their code is at
[lmullen/civil-procedure-codes](https://github.com/lmullen/civil-procedure-codes) (see
`scripts/corpus-lsh.R`); it uses Mullen's R package
[textreuse](https://docs.ropensci.org/textreuse/). We use their settings: 5-word phrases,
120 minhashes, 60 bands.

MinHash shrinks each passage to a 120-number signature whose overlap estimates Jaccard, and
locality-sensitive hashing (LSH) only compares passages whose signatures match on at least one
2-number band. Tested on 299,194 sections of North Carolina session laws, 03 took about a minute
(02 would need a day or more) and agreed with 02 on 601 of 646 pairs in a 1,274-section sample.

Differences from Funk and Mullen:

- **Boilerplate.** 03 first ignores any phrase found in more than `MAX_PASSAGES` passages
  (mastheads, headers, legal formulas). Their script has no such step.
- **Scores.** They computed the exact Jaccard similarity of every candidate pair. 03 uses the
  estimate MinHash gives for free (the share of the 120 signature numbers two passages have in
  common), typically within about 0.05.
- **Matches.** They kept matches scoring as low as 0.1 and, for each code, its best match from an
  earlier code. 03 keeps every pair at `MATCH` or above and links them into groups, without using
  dates, so it works on any corpus. Each group is led by its earliest passage in corpus order.

03 writes MinHash out by hand in a few lines of numpy so you can see how it works. The usual Python
library for it is [datasketch](https://ekzhu.com/datasketch/).

---

## Setup

From inside the `11-Text-Reuse` folder:

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt # installs numpy (only 03 needs it)
```

## Running it

```bash
source venv/bin/activate        # Windows: venv\Scripts\activate
python 01_reuse_jaccard_by_hand.py
python 02_reuse_all_pairs.py
python 03_reuse_minhash.py             # if you need it
python 04_reuse_trace_clause.py        # if you need it; opens a page in your browser
```

To follow a clause, copy a few distinctive words from 02's printout (or `output/02_pairs.csv`) into
`START` in 04. Results are saved in `output/`.

---

## Things to keep in mind

- **A score of 0 can be the right answer.** It means no pair reached `MATCH`, not that the script
  failed. Check that your passages are short enough before deciding there's no reuse.
- **Cut passages rarely line up.** `PASSAGE_WORDS` cuts every text at fixed points, so the same
  paragraph in two places gets cut differently and scores lower than it should. Try a lower `MATCH`
  (0.3) or a different `PASSAGE_WORDS` and see what changes.
- **Boilerplate looks like reuse.** Mastheads, page headers, and legal or institutional formulas
  repeat everywhere. 02 has no filter for them, so read past them at the top of its results. 03
  ignores phrases found in more than `MAX_PASSAGES` passages.
- **Copied often isn't the same as important.** The most-repeated text in a corpus is usually its
  formulas.
- **Groups chain.** If A matches B and B matches C, 03 puts all three in one group, even when A and
  C share little. Read a group's members before treating it as one text.
- **Earlier doesn't prove copying.** When two texts share a passage, the earlier one is only the
  earliest surviving version. Both may have copied something else.
- **OCR errors break n-grams.** One misread word breaks every phrase it sits in, and line-end
  hyphens split words in two ("mem- bers"). Character shingles cope better than word n-grams (try it
  in 01).
- **Numbers aren't words.** The phrase pattern keeps only letters, so dates, amounts and section
  numbers don't count.
