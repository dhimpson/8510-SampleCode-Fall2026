#!/usr/bin/env python3
"""
Step 0: Download the photographs
================================

Reads data/sample.csv and saves each photograph to images/. The sample is 400
photographs of feminist demonstrations, 1970-1981, by Bettye Lane and Freda
Leinwand, from the Schlesinger Library's "Catching the Wave" collection at
Harvard. Pro-life rallies are included. See the README for how they were chosen.

The quicker way is the Box download in the README. Use this script if that
link doesn't work. It gets the same 400 photos straight from Harvard.

Takes 10-15 minutes (Harvard's image server is slow). Photos you already have
are skipped, so if it stops partway, run it again.

Why the images aren't in the repository: each catalog record says the image
"may not be reproduced or transmitted in any form... without permission in
writing from the copyright holder." We use them for analysis in this class only
and keep them out of GitHub (images/ is in .gitignore). Please don't pass them on.
"""

import csv
import time
import urllib.request
from pathlib import Path

import cv2

SCRIPT_DIR = Path(__file__).parent

LONGEST_SIDE = 800   # Harvard sends most at about 770 pixels and a few at 5,000; shrink those to match
HEADERS = {"User-Agent": "Mozilla/5.0 (HIST8510 class research)"}


def main():
    with open(SCRIPT_DIR / "data" / "sample.csv", encoding="utf-8") as f:
        photos = list(csv.DictReader(f))

    (SCRIPT_DIR / "images").mkdir(exist_ok=True)
    for n, photo in enumerate(photos, 1):
        path = SCRIPT_DIR / photo["file"]
        if path.exists():
            continue
        req = urllib.request.Request(photo["image_url"], headers=HEADERS)
        for attempt in range(5):
            try:
                with urllib.request.urlopen(req, timeout=120) as resp:
                    path.write_bytes(resp.read())
                break
            except OSError as e:          # dropped connection: wait and try again
                print("  retry", attempt + 1, e)
                time.sleep(10)
        else:
            print(f"  skipped {photo['title'][:50]}: run the script again later")
            continue

        img = cv2.imread(str(path))
        longest = max(img.shape[:2])
        if longest > LONGEST_SIDE:
            scale = LONGEST_SIDE / longest
            img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
            cv2.imwrite(str(path), img)

        print(f"{n:3} of {len(photos)}  {photo['title'][:60]}")
        time.sleep(1)    # be polite to Harvard's image server

    have = sum((SCRIPT_DIR / p["file"]).exists() for p in photos)
    print(f"\n{have} of {len(photos)} photos are in images/")


if __name__ == "__main__":
    main()
