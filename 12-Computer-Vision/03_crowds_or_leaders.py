#!/usr/bin/env python3
"""
Step 3: Mass movement or famous leaders?
========================================

Did Bettye Lane picture second-wave feminism as crowds or as a few well-known
individuals, and did that change between 1970 and 1981?

Joins the boxes from step 2 to the catalog records in data/sample.csv:

  - dvt says how many people are in each photo and how tall the tallest is
  - the catalog says when the photo was taken and whether it names anyone

Each photo is sorted by how many people the model found:

    no people     0
    individual    1-2      (INDIVIDUAL)
    small group   3-9
    crowd         10+      (CROWD)

A "leader photo" is an individual photo whose catalog record names someone.
Few people alone isn't enough: some individual photos are close-ups of a sign.

Only Lane's photos by default: Freda Leinwand's catalog records never name
anyone, so they can't show leaders. The sample has extra Lane photos for
1970-73 and 1978-81, the two periods being compared; 1974-77 has fewer.

Change PERSON_SCORE, INDIVIDUAL, or CROWD and run it again. Nothing has to be
detected again: step 2 saved every box with its score.
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")                 # draw to a file, not a window
import matplotlib.pyplot as plt
import pandas as pd

SCRIPT_DIR = Path(__file__).parent

# --- Change these --------------------------------------------------------------

DETECTIONS = "data/detections.csv"   # all photos; your own run of step 2 is output/detections.csv
PHOTOGRAPHER = "Lane, Bettye"        # None = both photographers

PERSON_SCORE = 0.7    # count a box as a person if the model is at least this sure
INDIVIDUAL = 2        # this many people or fewer is an individual (or a pair)
CROWD = 10            # this many or more is a crowd

PERIODS = [(1970, 1973), (1974, 1977), (1978, 1981)]

# -------------------------------------------------------------------------------

KINDS = ["crowd", "small group", "individual", "no people"]
COLORS = ["#2b4c7e", "#5b8db8", "#d6781e", "#c5cad3"]
OUTPUT_FOLDER = SCRIPT_DIR / "output"


def kind(people):
    if people == 0:
        return "no people"
    if people <= INDIVIDUAL:
        return "individual"
    if people < CROWD:
        return "small group"
    return "crowd"


def period(year):
    for first, last in PERIODS:
        if first <= year <= last:
            return f"{first}-{last}"
    return None


def names_a_person(named):
    """The catalog lists the people and organizations shown, e.g.
    "Abzug, Bella S.; National Organization for Women". People are written
    Last, First, so a comma means a person."""
    if not isinstance(named, str):
        return False
    return any(", " in name for name in named.split("; "))


def give_or_take(share, n):
    """Roughly how far a share could be off by chance with only n photos
    (a 95% margin of error, in percentage points)."""
    return 196 * (share * (1 - share) / n) ** 0.5


def percent_table(rows, columns):
    table = pd.crosstab(rows, columns, normalize="index") * 100
    table = table.reindex(columns=[k for k in KINDS if k in table.columns])
    table["photos"] = rows.value_counts()
    return table.round(0).astype(int)


def main():
    boxes = pd.read_csv(SCRIPT_DIR / DETECTIONS)
    people = boxes[(boxes["label"] == "person") & (boxes["score"] >= PERSON_SCORE)]
    per_photo = people.groupby("id").agg(people=("score", "size"),
                                         tallest=("height_share", "max"))

    photos = pd.read_csv(SCRIPT_DIR / "data" / "sample.csv")
    photos = photos.rename(columns={"people": "named"})       # the catalog's names, not dvt's count
    photos = photos[photos["id"].isin(boxes["id"])]           # only photos step 2 looked at
    if PHOTOGRAPHER:
        photos = photos[photos["photographer"] == PHOTOGRAPHER]
    photos = photos.merge(per_photo, on="id", how="left")
    photos[["people", "tallest"]] = photos[["people", "tallest"]].fillna(0)
    photos["people"] = photos["people"].astype(int)
    photos["kind"] = photos["people"].apply(kind)
    photos["period"] = photos["year"].apply(period)
    photos["names a person"] = photos["named"].apply(names_a_person)
    photos["leader photo"] = (photos["kind"] == "individual") & photos["names a person"]

    who = " ".join(reversed(PHOTOGRAPHER.split(", "))) if PHOTOGRAPHER else "both photographers"
    print(f"{len(photos)} photos by {who}; a person = a box scored {PERSON_SCORE} or higher\n")

    print("1. What kind of photo, by period (% of each period's photos)\n")
    print(percent_table(photos["period"], photos["kind"]).to_string(), "\n")

    print("2. Leaders, by period\n")
    leaders = photos.groupby("period").agg(
        photos=("id", "size"),
        people_per_photo=("people", "mean"),
        names_a_person=("names a person", "mean"),
        leader_photos=("leader photo", "sum"))
    leaders["leader %"] = leaders["leader_photos"] / leaders["photos"] * 100
    leaders["give or take"] = [give_or_take(row["leader_photos"] / row["photos"], row["photos"])
                               for _, row in leaders.iterrows()]
    leaders["names_a_person"] *= 100
    leaders.columns = ["photos", "people per photo", "% naming a person",
                       "leader photos", "% leader photos", "give or take (points)"]
    print(leaders.round(1).to_string(), "\n")

    print("3. Check: does the catalog naming someone go with fewer people? (%)\n")
    named = photos["names a person"].map({True: "names a person", False: "names no one"})
    print(percent_table(named, photos["kind"]).to_string(), "\n")

    print("4. The leader photos, to check by eye\n")
    for _, p in photos[photos["leader photo"]].sort_values("year").iterrows():
        print(f"  {p['year']}  {p['people']} people  {p['title'][:50]:50}  {p['named'][:40]}")
    print()

    # Chart: kinds by period, and naming / leader photos by period
    by_period = pd.crosstab(photos["period"], photos["kind"], normalize="index") * 100
    by_period = by_period.reindex(columns=[k for k in KINDS if k in by_period.columns])
    fig, (left, right) = plt.subplots(1, 2, figsize=(12, 5),
                                      gridspec_kw={"width_ratios": [3, 2]})
    bottom = pd.Series(0.0, index=by_period.index)
    for k, color in zip(KINDS, COLORS):
        if k in by_period:
            left.bar(by_period.index, by_period[k], bottom=bottom, color=color, label=k)
            bottom += by_period[k]
    left.set_ylabel("% of photos")
    left.set_title(f"What kind of photo? (person = score {PERSON_SCORE}+)")
    left.legend(loc="upper left", bbox_to_anchor=(1, 1), frameon=False)

    x = range(len(leaders))
    right.bar([i - 0.2 for i in x], leaders["% naming a person"], width=0.4,
              color="#8e44ad", label="catalog names a person")
    right.bar([i + 0.2 for i in x], leaders["% leader photos"], width=0.4,
              yerr=leaders["give or take (points)"], capsize=4,
              color="#d6781e", label="leader photo (1-2 people, named)")
    right.set_xticks(list(x), leaders.index)
    right.set_ylabel("% of photos")
    right.set_title("Named people and leader photos")
    right.legend(loc="upper left", frameon=False)
    for ax in (left, right):
        ax.spines[["top", "right"]].set_visible(False)
    counts = ", ".join(f"{p}: {n}" for p, n in leaders["photos"].items())
    fig.suptitle(f"{who}, feminist demonstrations, 1970-1981 (photos per period: {counts})")
    fig.tight_layout()

    OUTPUT_FOLDER.mkdir(exist_ok=True)
    chart = OUTPUT_FOLDER / "crowds_or_leaders.png"
    fig.savefig(chart, dpi=150, bbox_inches="tight")
    photos.drop(columns=["image_url", "context_url"]).to_csv(
        OUTPUT_FOLDER / "photos_with_counts.csv", index=False)
    print(f"Saved {chart.relative_to(SCRIPT_DIR)} and output/photos_with_counts.csv")


if __name__ == "__main__":
    main()
