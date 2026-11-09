#!/usr/bin/env python3
"""
Step 2: Turn photographs into a table
=====================================

Runs dvt's object detector on every photograph in images/ and saves one row
per box it finds to output/detections.csv:

    id, label, score, height_share

height_share is how much of the photo's height the box fills (0 to 1). A
person filling 0.9 of the frame is a close-up; 0.2 is someone in a crowd.

It saves every box, however unsure the model is (scores go down to about
0.05). Deciding how sure is sure enough happens in step 3, so you can change
your mind there without running the model again. Annotate once, interpret
many times.

About 1 second per photo. Set LIMIT to None to do all 400 (about 8 minutes).
data/detections.csv is a finished run of all 400, which step 3 uses.
"""

import csv
import time
from pathlib import Path

import dvt

SCRIPT_DIR = Path(__file__).parent

# --- Change these --------------------------------------------------------------

LIMIT = 10        # how many photos to do; None = all of them
SHOW_SCORE = 0.7  # only for the summary printed below; every box is saved

# -------------------------------------------------------------------------------

OUTPUT_FOLDER = SCRIPT_DIR / "output"


def main():
    with open(SCRIPT_DIR / "data" / "sample.csv", encoding="utf-8") as f:
        photos = list(csv.DictReader(f))[:LIMIT]

    detector = dvt.AnnoDetect()
    rows = []
    start = time.time()
    for n, photo in enumerate(photos, 1):
        img = dvt.load_image(str(SCRIPT_DIR / photo["file"]))
        height = img.shape[0]
        found = detector.run(img)

        boxes = list(zip(found["labels"], found["scores"], found["y"], found["yend"]))
        for label, score, y, yend in boxes:
            rows.append({"id": photo["id"], "label": label, "score": round(float(score), 3),
                         "height_share": round((yend - y) / height, 3)})
        if not boxes:      # keep a row so the photo still counts, with no people
            rows.append({"id": photo["id"], "label": "(nothing)", "score": 0, "height_share": 0})

        people = sum(1 for label, score, _, _ in boxes
                     if label == "person" and score >= SHOW_SCORE)
        print(f"{n:3}. {people:3} people  {photo['year']}  {photo['title'][:60]}")

    seconds = time.time() - start
    print(f"\n{len(photos)} photos in {seconds:.0f} seconds ({seconds / len(photos):.1f} per photo)")

    OUTPUT_FOLDER.mkdir(exist_ok=True)
    out_path = OUTPUT_FOLDER / "detections.csv"
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "label", "score", "height_share"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"Saved {len(rows):,} boxes to {out_path.relative_to(SCRIPT_DIR)}")


if __name__ == "__main__":
    main()
