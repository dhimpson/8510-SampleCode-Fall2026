# Week 2 — Database Design

HIST 8510 · Methods in Digital History II · Fall 2026

A four-table SQLite database built from a slice of Bob Damron's Address Book,
South Carolina. Used in class Monday, and the pattern you will copy for your
own sources.

## Run order

```bash
python3 00_reset.py             # delete the database and start clean
python3 01_build_db.py          # create the tables, load the seed data
python3 02_insert_a_venue.py    # add one record, one SQL statement at a time
python3 03_break_a_foreign_key.py   # watch a bad insert succeed silently
```

Then open `sc_guides.db` in DBcode and look around.

`00_reset.py --rebuild` does the first two in one step.

## What is in here

| File | What it is |
|---|---|
| `01_create_schema.sql` | **The one to actually read.** Four tables, and the argument for each decision in the comments. |
| `01_build_db.py` | Thin runner. Turns on foreign keys, runs the schema, loads the CSVs. |
| `02_insert_a_venue.py` | Adds one venue slowly, printing every SQL statement before it runs. Safe to re-run. |
| `03_break_a_foreign_key.py` | Runs the same bad INSERT with enforcement on, then off. Leaves a broken row on purpose. |
| `00_reset.py` | Deletes `sc_guides.db`. Reports what was in it first. |
| `00_flat_table.csv` | The same data as one wide sheet, with `type_1`, `type_2`, `type_3` columns. The problem, before the fix. |
| `seed/` | The four tables as CSVs, already normalized. |
| `make_seed.py` | How `seed/` was derived from `sc-data.csv`. Not run in class. |
| `sc-data.csv` | The full South Carolina slice, 1,396 listings, 1965 to 2003. |
| `schema_diagram.md` | Mermaid ERD. Copy this convention for your own documentation. |
| `schema_starter/` | Copy this folder to start your own schema. |

## The four tables

- **cities** — one row per city. In the flat sheet "Charleston" is retyped on
  every listing; here it exists once and gets pointed at.
- **venue_types** — the categories Damron used, kept exactly as printed.
- **venues** — one row per *listing*, meaning one venue in one guide year.
- **venue_type_link** — the junction table. Two foreign keys, one row per pairing.

## Two things worth knowing before you build your own

**The type vocabulary is not clean, and we did not clean it.** This database
contains `Bars`, `Bars/Clubs`, `Bars & Nightclubs`, and `Nightclubs`. It also
contains both `Cruising Areas` and `Cruisy Areas`. Those are not transcription
errors. The guides ran for nearly forty years and their own vocabulary moved.
Merging them makes counting easier and erases the change; keeping them apart
preserves the change and makes counting harder. Neither is correct. Your
schema is where you record which you chose, and your README is where you say
why. (Rawson and Muñoz, "Against Cleaning.")

**One row is one listing, not one venue.** Bushwacker's Pub in Greenville
appears in eight editions and is therefore eight rows. The alternative —
one venue with eight listings attached — is truer to the sources and needs a
fifth table. We built the simpler version, and it costs us something real: to
follow a single venue across time you have to match on title and city, and
titles in this data are not reliable. The full file has both
`Beach at 82nd Ave.` and `Beach at 82nd Ave`, one period apart, as separate
places.

That trade is the whole point. A schema is not a neutral container you pour
sources into. It is a claim about what the sources are, made before any
analysis starts, and it decides which questions you will be able to ask.

## Source

Data from [Mapping the Gay Guides](https://www.mappingthegayguides.org/),
Amanda Regan and Eric Gonzaba. South Carolina entries from Bob Damron's
Address Book, 1965 to 2003.
