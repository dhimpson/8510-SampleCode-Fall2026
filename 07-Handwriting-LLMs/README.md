# Handwriting Transcription with LLMs

This week we transcribe handwritten documents with Gemini Flash-Lite, then measure how
accurate the transcriptions are using **character error rate (CER)** and **word error rate (WER)**.

| Script | What it does | Needs API key? |
|---|---|---|
| `01_cer_wer_demo.py` | Shows how CER and WER work on short examples | No |
| `02_gemini_transcribe.py` | Sends every image in `images/` to Gemini, saves transcriptions | Yes |
| `03_evaluate.py` | Compares transcriptions to `ground-truth/` and scores them | No |

---

## Setup

### Step 1: Put your API key in a `.env` file

From inside the `07-Handwriting-LLMs` folder:

```bash
cp .env.example .env
```

Open `.env` and replace `your-api-key-here` with your key (the same one from last week).

### Step 2: Create a virtual environment and install packages

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## The folders

```
images/          handwriting images (.jpg, .png, .webp)
ground-truth/    a hand-checked transcription for each image
ocr-results/     Gemini's transcriptions, one folder per run (created by script 02)
evaluation/      scores and alignments (created by script 03)
```

**File names must match.** The ground truth for `images/letter1.jpg` goes in
`ground-truth/letter1.txt`. Script 02 saves Gemini's version as `ocr-results/baseline/letter1.txt`.

---

## Transcription conventions

The ground truth and the prompt must follow **the same rules**, or CER measures the
difference between two sets of rules instead of reading accuracy.

- Keep original spelling, capitalization, punctuation and abbreviations. Don't correct or expand anything.
- Start a new line wherever the writer did.
- Crossed-out words: `[crossed out: word]`, or `[crossed out]` if unreadable
- Words added above or below the line: put them in place as `[inserted: word]`
- Unreadable words: `[illegible]`
- Uncertain readings: `word[?]`

If you change these rules, change them in both places: the `PROMPT` in
`02_gemini_transcribe.py` and your ground-truth files.

---

## Running it

```bash
source venv/bin/activate
python 01_cer_wer_demo.py
python 02_gemini_transcribe.py
python 03_evaluate.py
```

### Reading the scores

`03_evaluate.py` gives two scores for each page:

- **Raw:** the exact text. Case, punctuation and line breaks all count as errors.
- **Normalized:** lowercase, punctuation removed, line breaks ignored. Only the words count.

If the raw score is much worse than the normalized one, most of the "errors" are formatting,
not misreadings. (Occasionally the normalized score is slightly *higher*; removing punctuation
makes the page shorter, so each remaining error counts for more.)

To see exactly which words were wrong, open `evaluation/<run>/<page>_alignment.txt`.
All the scores are also saved to `evaluation/results.csv`.

---

## Experiments

At the top of `02_gemini_transcribe.py` you can change:

- `MODEL`: for example, try `gemini-2.5-flash-lite` (cheaper, older)
- `THINKING_LEVEL`: `"minimal"`, `"low"`, `"medium"` or `"high"`
- `PROMPT`: for example, delete the "do not correct" rule

**Give each experiment a new `RUN_NAME`** so it doesn't overwrite earlier results. Then run
`03_evaluate.py`, which scores every run and prints a comparison table.

Also try running the same settings twice under two run names. Do you get the same transcription?

## Results of entire exercise (this is a Claude synopsis):
Baseline vs. baseline-2: The normalized scores are identical, but raw WER went from 12.5% to 10.4%, a difference of one word. With identical settings, the model produced slightly different output, probably a line break or punctuation mark. That's your measure of random variation: a one-word difference between runs could just be chance.

Context prompt: This is identical to baseline-2. Telling the model the letter's date made no measurable difference on this page.

High thinking: This is the best normalized score, but only by one word and one character. That fits the idea that more thinking helps a little, but it's within the range of chance, and this run's raw score is actually the worst. It also cost more.

No verbatim rule: This is the most interesting result. It has the best raw score (6.2%) but the worst normalized CER (0.8%). One possible explanation is that it handled formatting and line breaks better but changed an extra letter somewhere, perhaps "correcting" a spelling. Open evaluation/no-vebatim-rule/IMG_0376_alignment.txt to check what it did with "Defintely."

Raw vs. normalized: In every run, raw WER is 2 to 5 times higher than normalized WER. So most of the model's "errors" are formatting, such as case, punctuation, and line breaks, not misreading the handwriting.

Overall: Gemini read this letter almost perfectly, missing only 2 or 3 words out of 65, whichever settings you used. With one page, none of the experiments shows a difference larger than normal run-to-run variation. If you want stronger conclusions, adding ground truth for one or two more pages, especially harder ones, would help the most.