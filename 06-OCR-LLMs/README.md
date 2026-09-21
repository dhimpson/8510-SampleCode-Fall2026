# OCR with LLMs (Gemini)

Last week we used Tesseract, which recognizes characters and needed careful image
preprocessing to work well. This week we give the raw image to a multimodal LLM
(Google's Gemini Flash-Lite) and ask it to transcribe the page.

`gemini_ocr.py` sends every image in `images/` to Gemini and asks for a **verbatim**
transcription that preserves the layout: columns, line breaks, and spacing. Each result
is saved as a `.txt` file in `ocr-results/`. The script prints the tokens and cost for
each image, plus a total at the end.

The sample images are the same ones from Week 5, so you can compare the Tesseract output
with Gemini's output directly.

---

## Setup

### Step 1: Get an API key

Go to <https://aistudio.google.com/apikey>, sign in with a Google account, and create a key.

### Step 2: Put the key in a `.env` file

From inside the `06-OCR-LLMs` folder:

```bash
cp .env.example .env
```

Open `.env` and replace `your-api-key-here` with your key. The `.env` file is listed in
`.gitignore`, so it won't be committed. **Never paste your key directly into the script.**

### Step 3: Create a virtual environment and install packages

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Unlike Week 5, there's nothing to install with Homebrew. The OCR happens on Google's servers.

---

## Running it

```bash
python gemini_ocr.py
```

Example output (your numbers will differ):

```
Transcribing IMG_0402.jpg ...
  Saved to ocr-results/IMG_0402.txt
  Input tokens:    1,290
  Output tokens:   812
  Thinking tokens: 0
  Cost:            $0.002417
```

To OCR your own documents, drop `.jpg`, `.png`, or `.webp` files into `images/` and run it again.

---

## Things to notice

- **Tokens and cost.** Input tokens are the image plus the prompt. Output tokens are the
  transcription. Output costs much more per token than input.
- **Thinking tokens.** Gemini may "think" before it answers. You're billed for those
  tokens at the output rate even though you never see them, so the script counts them in the cost.
- **Prices change.** The prices are set at the top of `gemini_ocr.py`. Check
  [Google's pricing page](https://ai.google.dev/gemini-api/docs/pricing).
- **Verbatim isn't guaranteed.** LLMs are trained to produce fluent text, so they sometimes
  "fix" spellings, expand abbreviations, or fill in words they can't read. Unlike Tesseract,
  the result looks plausible even when it's wrong. Always check the output against the image.
- **Try changing the prompt.** The `PROMPT` variable controls how the model handles
  columns, tables, and illegible text. See what changes when you edit it.
