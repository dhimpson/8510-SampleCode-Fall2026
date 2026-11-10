# Computer Vision: Distant Viewing

Words come with a code we can count: letters, spaces, a dictionary. Images don't. Before a
computer can "read" a photograph, someone has to decide what to look for, and that decision is
already an interpretation. Taylor Arnold and Lauren Tilton call this **distant viewing**, and
their [Distant Viewing Toolkit](https://github.com/distant-viewing/dvt) (dvt) is what we use
this week.

Our question: **did photographers of the women's movement picture it as a mass movement or as a
few famous leaders, and did that change between 1970 and 1981?**

| Script | What it does |
|---|---|
| `00_download_images.py` | Downloads the 400 photographs in `data/sample.csv` from Harvard to `images/` (10-15 minutes). Only needed if you can't use the Box download below |
| `01_look_at_one_photo.py` | Runs dvt's object detector on one photo and saves a copy with every box labeled. Change `PHOTO` and `MIN_SCORE` |
| `02_annotate_photos.py` | Runs the detector on many photos and saves every box to `output/detections.csv`. `LIMIT = 10` by default; `None` does all 400 (about 8 minutes) |
| `03_crowds_or_leaders.py` | Counts people in each photo, sorts photos into crowds, small groups, and individuals, finds "leader photos" (1-2 people, and the catalog names someone), and compares three periods. Change `PHOTOGRAPHER`, `PERSON_SCORE`, `INDIVIDUAL`, and `CROWD` |

`data/detections.csv` is a finished run of step 2 on all 400 photos, so step 3 works right away.

## The photographs

The photographs are from **"Catching the Wave,"** the Schlesinger Library's digitized collection
of women's movement photographs by **Bettye Lane** and **Freda Leinwand** (Harvard), taken mostly
in New York and Washington, D.C. We got the catalog records from Harvard's public
[LibraryCloud API](https://library.harvard.edu/services-tools/harvard-library-apis-datasets).

- **`data/records.csv`**: the catalog record for all 7,483 photographs in the collection: title,
  photographer, year, subject headings (`topics`), people and organizations shown (`people`),
  sign text written out by catalogers (`abstract`), copyright holder, and image link.
- **`data/sample.csv`**: the 400 we use. Each has the subject heading "demonstrations" plus a
  feminist or abortion-related heading, from 1970 to 1981 (pro-life rallies included). The `draw`
  column says how each was chosen:
  - **`even`** (200): about 17 a year, both photographers.
  - **`extra Lane`** (200): 100 more Lane photos each from 1970-73 and 1978-81, the two periods
    we compare. Freda Leinwand's catalog records never name anyone in the photo, so only Lane's can
    show leaders; and "individual" photos are rare, so we needed more photos to count them.

  That gives Lane 150 photos for 1970-73, 61 for 1974-77, and 147 for 1978-81 (Leinwand: 42 in
  all). The `file` column says where step 0 saves the image.

**Rights.** Harvard releases its catalog records under CC0 and asks that you credit Harvard Library
and the Schlesinger Library, so the CSV files are in this repository. The **images are not**: each
record says the image "may not be reproduced or transmitted in any form... without permission in
writing from the copyright holder" (the Estate of Bettye Lane or of Freda Leinwand). We share them
through Box for analysis in this class only. Keep them out of GitHub (`images/` and `*.zip` are in
`.gitignore`), and don't pass them on.

## Setup

### Step 1: Create the virtual environment

From inside the `12-Computer-Vision` folder:

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt # PyTorch, OpenCV, pandas, matplotlib, and dvt: about 1 GB
```

### Step 2: Get the photographs

**[Download the photographs from Box](https://clemson.box.com/s/5f7zuzypoyecz942vg24me7io23l1don)** (`catching-the-wave-images.zip`, 38 MB; sign in with your Clemson account).
Unzip it inside the `12-Computer-Vision` folder. You should end up with a folder called `images`
right next to the scripts, holding 400 `.jpg` files:

```
12-Computer-Vision/
├── 00_download_images.py
├── ...
├── data/
└── images/
    ├── urn-3_RAD.SCHL_13146401.jpg
    └── ... (400 photos)
```

On Windows, "Extract All" puts everything in an extra folder named after the zip file. Move the
`images` folder up so it sits next to the scripts, then delete the zip.

**If the Box link doesn't work,** download the same photographs from Harvard instead:

```bash
python 00_download_images.py
```

The first time you run step 1 or 2, dvt also downloads its object detection model (170 MB).

---

## Running it

```bash
python 01_look_at_one_photo.py    # one photo, every box drawn: see output/
python 02_annotate_photos.py      # 10 photos by default, about 12 seconds
python 03_crowds_or_leaders.py    # the question, using data/detections.csv
```

## Things to keep in mind

- **The model can only name 80 things.** dvt's detector learned from COCO, a 2014 set of everyday
  photographs. It has "person," "handbag," "tie," and "kite," but no sign, banner, button, or podium.
  At the 1978 ERA march it calls the suffrage-colored banners kites; at a 1981 rally "I'm pro-choice"
  balloons are sports balls. Whatever we count, we count through someone else's list of categories.
- **Crowds are undercounted.** The model returns at most 100 boxes per photo (57 of our 400 hit that
  limit) and misses small, overlapping, or half-hidden people. A packed 1970 rally of well over a
  hundred comes back as 32 people at a 0.5 cutoff. So "crowd" (10 or more) is a floor, and people per photo is lower than it should be.
- **The cutoff decides the answer.** `PERSON_SCORE` changes how many crowds there are: 65% of Lane's
  1970-73 photos are crowds at 0.5, 53% at 0.7, and 19% at 0.9. Compare periods at the same cutoff,
  and check whether a pattern survives a change of cutoff before you believe it.
- **Photos come in bunches.** A photographer shoots a whole roll at one rally. Lane's 150 photos from
  1970-73 come from only about 47 events, and the 1978-81 leader photos from about 7. Photos from the
  same event aren't independent, so the "give or take" in step 3 is too small: the real uncertainty is
  larger.
- **A name in the record may not be the person in the frame.** The catalog often lists everyone at
  an event on every photo from it (every photo from the 1978 ERA march in Washington names Margaret
  Costanza, Gloria Steinem, and others). "Names a person" means a named person was there, not
  necessarily in this picture.
- **Few people doesn't mean a leader.** Some "individual" photos are portraits of someone well known;
  others are close-ups of a sign with a hand holding it. Look at the photos (step 1, or the list step 3
  prints) before deciding what a category means.
- **The catalog has its own point of view.** Who is named comes from the photographers' captions and
  from catalogers decades later. Freda Leinwand's records never name anyone, which is why step 3 uses
  only Lane's photos (358 of the 400), mostly taken in New York.
- **We don't use face recognition.** dvt can match faces across photos, but most people here were
  private citizens at protests about abortion and sexuality, photographed without any idea they'd be
  searchable. Identifying them is a kind of surveillance we chose not to do.

## Taking it further

- **Train your own detector.** dvt only uses models that are already trained, but its detector is a
  standard PyTorch model (Faster R-CNN). Draw boxes around protest signs on a few hundred photos (in a
  labeling tool like [Label Studio](https://labelstud.io/)) and fine-tune the model to find them.
  Expect hours of labeling and training.
- **Describe what you're looking for.** Models such as OWLv2 and Grounding DINO (on Hugging Face) find
  things from a typed phrase, like "protest sign," without any training.
- **Ask Gemini.** It can count the signs in a photo and read them, as in Weeks 6 and 8.

## Sources

- Taylor Arnold and Lauren Tilton, *Distant Viewing: Computational Exploration of Digital Images*
  (MIT Press, 2023), open access; and "Distant Viewing: Analyzing Large Visual Corpora,"
  *Digital Scholarship in the Humanities* 34, suppl. 1 (2019), doi:10.1093/llc/fqz013.
- [Distant Viewing Toolkit](https://github.com/distant-viewing/dvt), with tutorials.
- [Catching the Wave](https://guides.library.harvard.edu/schlesinger/catchingthewave): Bettye Lane and
  Freda Leinwand photographs, Schlesinger Library, Radcliffe Institute, Harvard University.
