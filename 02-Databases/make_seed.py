"""
make_seed.py  —  How the seed CSVs were made
HIST 8510  ·  Week 2  ·  Database Design

You do NOT need to run this for class. The seed/ CSVs are already built.

This script exists so the normalization is inspectable rather than magic. It
takes the flat file (sc-data.csv, one row per guide listing, with a `type`
column that sometimes holds several comma-separated categories) and splits it
into the four tables our schema expects.

The interesting work is in step 4, where one `type` cell like

    "Book Store,Cruising Areas,Erotic Shop"

becomes three rows in venue_type_link. That is the flattening being undone.

A note on what this script deliberately does NOT do
---------------------------------------------------
It does not merge "Bars" with "Bars/Clubs", or "Cruising Areas" with
"Cruisy Areas". Those look like inconsistencies and they are not: Damron's
own vocabulary changed across nearly forty years of guides. Merging them
would make counting easier and would quietly erase the change. We keep the
guide's words and leave the decision to the historian. See Rawson and Munoz,
"Against Cleaning."

Run it with:  python3 make_seed.py
"""

import csv
import os

SOURCE = "sc-data.csv"
SEED_DIR = "seed"

# ---------------------------------------------------------------- the subset
# Ten venues across six cities. This is a curated subset, not a random sample.
# Only 71 of the 1,396 rows in the full South Carolina file carry more than one
# type, so a random sample would mostly miss the thing we are here to teach.
#
# Each of these was chosen for a reason:
DEMO_VENUES = [
    # (title, city)                                 why it is here
    ("Bushwacker's Pub", "Greenville"),           # 8 years, 8 different codings
    ("Time Out", "Myrtle Beach"),                 # "Bars", "Bars/Clubs", "Bars & Nightclubs"
    ("Cheyenne Cattlemen's Club", "Spartanburg"), # same drift, no commas involved
    ("Hurl Rock Park", "Myrtle Beach"),           # "Cruising Areas" becomes "Cruisy Areas"
    ("Streetcar", "Charleston"),                  # multi-type
    ("Holiday Inn Bar", "Florence"),              # multi-type
    ("Adult World", "Spartanburg"),               # three categories in one cell
    ("Richland Adult Books", "Columbia"),         # multi-type, and the pair reorders
    ("Hilltop Adult Bookstore", "Greenville"),    # multi-type
    ("Cheeks", "Charleston"),                     # multi-type
]


def main():
    if not os.path.exists(SOURCE):
        raise SystemExit(f"Cannot find {SOURCE}. It should sit beside this script.")
    os.makedirs(SEED_DIR, exist_ok=True)

    # 1 ---------------------------------------------------- read the flat file
    with open(SOURCE, encoding="utf-8") as f:
        all_rows = list(csv.DictReader(f))

    wanted = set(DEMO_VENUES)
    rows = [
        r for r in all_rows
        if ((r["title"] or "").strip(), (r["city"] or "").strip()) in wanted
    ]
    rows.sort(key=lambda r: ((r["city"] or "").strip(),
                             (r["title"] or "").strip(),
                             int(r["Year"])))
    print(f"Selected {len(rows)} listings for {len(wanted)} venues.")

    # 2 -------------------------------------------------------------- cities
    # Every distinct city becomes one row. In the flat file "Charleston"
    # is repeated on every listing; here it is stored once and pointed at.
    city_ids = {}
    for r in rows:
        key = ((r["city"] or "").strip(), (r["state"] or "").strip())
        if key not in city_ids:
            city_ids[key] = len(city_ids) + 1

    write_csv(f"{SEED_DIR}/cities.csv", ["city_id", "city_name", "state"], [
        [cid, name, state] for (name, state), cid in sorted(city_ids.items(), key=lambda kv: kv[1])
    ])

    # 3 --------------------------------------------------------- venue_types
    # Split every type cell on commas, strip whitespace, and keep the
    # distinct labels EXACTLY as the guide printed them.
    type_ids = {}
    for r in rows:
        for label in split_types(r["type"]):
            if label not in type_ids:
                type_ids[label] = len(type_ids) + 1

    write_csv(f"{SEED_DIR}/venue_types.csv", ["type_id", "type_label"], [
        [tid, label] for label, tid in sorted(type_ids.items(), key=lambda kv: kv[1])
    ])

    # 4 -------------------------------------------------- venues + junction
    # One row per LISTING, meaning one row per venue per guide year.
    # See the note in 01_create_schema.sql about what that choice costs.
    venue_rows, link_rows = [], []
    for i, r in enumerate(rows, start=1):
        city_id = city_ids[((r["city"] or "").strip(), (r["state"] or "").strip())]
        venue_rows.append([
            i,
            (r["title"] or "").strip(),
            int(r["Year"]),
            (r["unique.id"] or "").strip(),
            (r["streetaddress"] or "").strip(),
            (r["description"] or "").strip(),
            city_id,
        ])
        # here is the flattening being undone: one cell becomes N rows
        for label in split_types(r["type"]):
            link_rows.append([i, type_ids[label]])

    write_csv(f"{SEED_DIR}/venues.csv",
              ["venue_id", "title", "year", "source_id",
               "street_address", "description", "city_id"], venue_rows)
    write_csv(f"{SEED_DIR}/venue_type_link.csv", ["venue_id", "type_id"], link_rows)

    # 5 ------------------------------------------------- the "before" picture
    # The same data as one wide sheet, so we can look at the failure in class
    # before we look at the fix.
    # Note that the columns keep the guide's original comma order. That order
    # carries no meaning, which is exactly the problem worth showing.
    id_to_city = {cid: name for (name, state), cid in city_ids.items()}
    flat = []
    for row, r in zip(venue_rows, rows):
        labels = split_types(r["type"])[:3]
        labels = labels + [""] * (3 - len(labels))
        flat.append([row[1], id_to_city[row[6]], row[2]] + labels)
    write_csv("00_flat_table.csv",
              ["title", "city", "year", "type_1", "type_2", "type_3"], flat)

    print(f"  cities           {len(city_ids):3d}")
    print(f"  venue_types      {len(type_ids):3d}")
    print(f"  venues           {len(venue_rows):3d}")
    print(f"  venue_type_link  {len(link_rows):3d}")
    print("\nWrote seed/*.csv and 00_flat_table.csv")


def split_types(cell):
    """'Book Store,Cruising Areas' -> ['Book Store', 'Cruising Areas']"""
    if not cell:
        return []
    return [part.strip() for part in cell.split(",") if part.strip()]


def write_csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


if __name__ == "__main__":
    main()
