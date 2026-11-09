#!/usr/bin/env python3
"""
Step 1: What does the computer see in one photograph?
=====================================================

Runs dvt's object detector on one photograph and saves a copy with a box
around everything it found. Each box is labeled with what the model thinks
the thing is and how sure it is (a score from 0 to 1).

The detector is a Faster R-CNN model trained on COCO, a 2014 collection of
everyday photographs labeled with 80 kinds of things: person, car, handbag,
tie, umbrella, kite, frisbee... It can only ever answer with one of those 80
labels. There is no "sign", "banner", or "podium", so watch what it calls them.

Change PHOTO (any file name in images/) and MIN_SCORE and run it again.
"""

import csv
from collections import Counter
from pathlib import Path

import cv2
import dvt

SCRIPT_DIR = Path(__file__).parent

# --- Change these --------------------------------------------------------------

PHOTO = "URN-3_RAD.SCHL_100515385.jpg"   # ERA march, Washington, D.C., 1978
MIN_SCORE = 0.5                          # only show boxes the model is at least this sure about

# Others worth trying:
#   "urn-3_RAD.SCHL_16091949.jpg"    women's liberation rally, 1970: a packed crowd
#   "URN-3_RAD.SCHL_100512698.jpg"   Labor Day abortion rights demonstration, 1981: "I'm pro-choice" balloons
#   "urn-3_RAD.SCHL_13147142.jpg"    welfare march, 1972: a hand-lettered sign, close up
#   "urn-3_RAD.SCHL_13146401.jpg"    Betty Friedan at the Women's Strike march, 1970

# -------------------------------------------------------------------------------

PERSON_COLOR = (47, 125, 107)    # teal (colors are red, green, blue)
OTHER_COLOR = (214, 120, 30)     # orange
OUTPUT_FOLDER = SCRIPT_DIR / "output"


def catalog_record(photo):
    """The photo's row in data/sample.csv, for its title and year."""
    with open(SCRIPT_DIR / "data" / "sample.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if Path(row["file"]).name == photo:
                return row
    return {"title": "(not in sample.csv)", "year": ""}


def draw_box(img, x, y, xend, yend, text, color):
    """A rectangle with a small filled label above its top-left corner."""
    cv2.rectangle(img, (x, y), (xend, yend), color, 2)
    (w, h), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.45, 1)
    top = max(y - h - 6, 0)
    cv2.rectangle(img, (x, top), (x + w + 4, top + h + 6), color, -1)
    cv2.putText(img, text, (x + 2, top + h + 2), cv2.FONT_HERSHEY_SIMPLEX,
                0.45, (255, 255, 255), 1, cv2.LINE_AA)


def main():
    record = catalog_record(PHOTO)
    print(f"{PHOTO}\n{record['title']} ({record['year']})\n")

    img = dvt.load_image(str(SCRIPT_DIR / "images" / PHOTO))   # an array of pixels: height x width x 3 colors
    height, width = img.shape[:2]
    print(f"The image is {width} x {height} pixels.")

    detector = dvt.AnnoDetect()       # downloads the model (170 MB) the first time
    found = detector.run(img)         # boxes, labels, and scores for everything it found

    boxes = zip(found["labels"], found["scores"],
                found["x"], found["y"], found["xend"], found["yend"])
    kept = [b for b in boxes if b[1] >= MIN_SCORE]
    print(f"The model returned {len(found['labels'])} boxes; "
          f"{len(kept)} have a score of at least {MIN_SCORE}.\n")

    for label, score, x, y, xend, yend in sorted(kept, key=lambda b: -b[1]):
        print(f"  {score:.2f}  {label}")
        color = PERSON_COLOR if label == "person" else OTHER_COLOR
        draw_box(img, int(x), int(y), int(xend), int(yend), f"{label} {score:.2f}", color)

    print("\nCounts:", dict(Counter(b[0] for b in kept)))

    OUTPUT_FOLDER.mkdir(exist_ok=True)
    out_path = OUTPUT_FOLDER / f"boxes_{Path(PHOTO).stem}.jpg"
    dvt.save_image(str(out_path), img)
    print(f"\nSaved {out_path.relative_to(SCRIPT_DIR)}")


if __name__ == "__main__":
    main()
