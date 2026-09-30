## Version 1 – Original prompt (baseline)
Prompt:
```PROMPT = """Transcribe all of the text in this image exactly as it appears on the page.

Rules:
- Transcribe verbatim. Do NOT correct spelling, grammar, punctuation, or capitalization.
  Keep errors, abbreviations, and archaic spellings exactly as written.
- Do NOT summarize, paraphrase, translate, or add anything that is not on the page.
- Preserve the layout: keep the original line breaks, indentation, and blank lines.
- If the page has multiple columns of running text, transcribe the full left column
  from top to bottom, then the next column, and so on.
- If the page has a table or form, keep each row on its own line and use spaces
  to line the columns up the way they appear on the page.
- Include headers, footers, page numbers, marginal notes, stamps, and handwriting.
- If a word or character cannot be read, write [illegible] in its place.
  Do not guess.
- Output only the transcription: no introduction, no commentary, no markdown formatting."""
```
Date: Sept 23, 2026
Images: 1960_AnnSt_part1.jpg, 1960_AnnSt_part2.jpg
What I changed: Nothing (professor's original rules, this run is my baseline.)
Why: Baseline for comparison
Output folder: results-v1-original
Tokens / cost: 
Saved to ocr-results/1960_AnnSt _part1.txt
  Input tokens:    1,316
  Output tokens:   248
  Thinking tokens: 0
  Cost:            $0.001015
  Saved to ocr-results/1960_AnnSt_part2.txt
  Input tokens:    1,295
  Output tokens:   51
  Thinking tokens: 0
  Cost:            $0.000516

Observations:  kept phone numbers, interpreted phone symbol as triangle, captured race indicator

## Version 2 - 
This version adds to the provided prompt and tells gemini to keep all symbols exactly as printed. This is important because a symbol that looks like a bullseye depicts homeowner. 

PROMPT = """Transcribe all of the text in this image exactly as it appears on the page.

Rules:
- Transcribe verbatim. Do NOT correct spelling, grammar, punctuation, or capitalization.
  Keep errors, abbreviations, and archaic spellings exactly as written.
- Do NOT summarize, paraphrase, translate, or add anything that is not on the page.
- Preserve the layout: keep the original line breaks, indentation, and blank lines.
- If the page has multiple columns of running text, transcribe the full left column
  from top to bottom, then the next column, and so on.
- If the page has a table or form, keep each row on its own line and use spaces
  to line the columns up the way they appear on the page.
- Include headers, footers, page numbers, marginal notes, stamps, and handwriting.
- If a word or character cannot be read, write [illegible] in its place.
  Do not guess.
 - Keep all symbols exactly as printed, including ◎ and Δ. Do not drop, replace,
  or explain them. 
- Output only the transcription: no introduction, no commentary, no markdown formatting."""

Date: Sept 23, 2026
Images: 1960_AnnSt_part1.jpg, 1960_AnnSt_part2.jpg
What I changed: I added a rule which said to not change any special characters or try to interpret them
Why:These directories carry special characters to denote homeowner and phone number. I need the homeowner denotation for my research.
Output folder: results-v2-original
Tokens / cost: 

Total input tokens:     1,316
Total output tokens:    241  (includes thinking)
Total cost:             $0.000997