"""
03_break_a_foreign_key.py  —  The failure that does not announce itself
HIST 8510  ·  Week 2  ·  Database Design

Runs the SAME bad INSERT twice: once with foreign key enforcement on,
once with it off. Watch the difference.

This script deliberately leaves a broken row in your database. That is
the whole point — the row is still there afterward, and nothing will
ever tell you. Run 00_reset.py when you are done.

Run it with:  python3 03_break_a_foreign_key.py
Clean up:     python3 00_reset.py --rebuild
"""

import sqlite3

DB_FILE = "sc_guides.db"

BAD_INSERT = """
INSERT INTO venues (title, year, city_id)
VALUES ('The Ghost Bar', 1981, 999);
"""


def show(sql):
    for ln in sql.strip("\n").rstrip().split("\n"):
        print("    " + ln)
    print()


def main():
    print("=" * 66)
    print("  The same bad INSERT, twice")
    print("=" * 66)
    print("""
Here is the statement we are going to run. It adds a venue in city_id
999. There is no city 999 — the cities table has six rows, numbered 1
to 6. So this statement is asking the database to store a venue in a
city that does not exist.""")
    show(BAD_INSERT)

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # ---------------------------------------------------------------
    print("-" * 66)
    print("ATTEMPT 1  ·  PRAGMA foreign_keys = ON")
    print("-" * 66)
    print("""
The schema declares FOREIGN KEY (city_id) REFERENCES cities (city_id).
With enforcement on, SQLite checks that promise on every insert.
""")

    cursor.execute("PRAGMA foreign_keys = ON")
    try:
        cursor.execute(BAD_INSERT)
        conn.commit()
        print("  Inserted. (If you are seeing this, the pragma did not take.)")
    except sqlite3.IntegrityError as e:
        print(f"  sqlite3.IntegrityError: {e}")
        print("""
  Refused. The database read the FOREIGN KEY line in your schema,
  checked cities for a row with city_id 999, did not find one, and
  rejected the statement. This is the behavior you want.""")
        # Clear the failed statement's transaction. PRAGMA foreign_keys is
        # ignored while a transaction is open, so this has to happen before
        # we can turn enforcement off below.
        conn.rollback()

    # ---------------------------------------------------------------
    print("\n" + "-" * 66)
    print("ATTEMPT 2  ·  PRAGMA foreign_keys = OFF   (SQLite's default)")
    print("-" * 66)
    print("""
Now the same statement again, with enforcement off. Nothing about the
schema has changed. The FOREIGN KEY line is still sitting there in
01_create_schema.sql. It is simply not being checked.
""")

    cursor.execute("PRAGMA foreign_keys = OFF")
    cursor.execute(BAD_INSERT)
    conn.commit()
    print("  (no output)")
    print("""
  It worked. No error, no warning, no return value to inspect. If this
  were inside a loop importing three thousand rows, you would have no
  way of knowing it had happened.""")

    # ---------------------------------------------------------------
    print("\n" + "-" * 66)
    print("SO WHERE DID IT GO?")
    print("-" * 66)
    print("""
A LEFT JOIN keeps every row from the left table even when the right
table has no match, filling the missing side with NULL. Asking for the
rows where the match came back NULL is how you find orphans.
""")

    orphan_query = """
SELECT v.venue_id, v.title, v.year, v.city_id
  FROM venues v
  LEFT JOIN cities c ON v.city_id = c.city_id
 WHERE c.city_id IS NULL;
"""
    show(orphan_query)
    orphans = cursor.execute(orphan_query).fetchall()

    for venue_id, title, year, city_id in orphans:
        print(f"  venue_id {venue_id}  ·  '{title}' ({year})  ·  city_id {city_id}")

    print(f"""
  {len(orphans)} row(s) pointing at a city that does not exist.

  That row is in your venues table. COUNT(*) will include it. But it
  will never appear in any query that JOINs venues to cities, because
  there is nothing to join it to. So your totals and your maps now
  disagree, and neither one is flagged as wrong.""")

    conn.close()

    print("\n" + "=" * 66)
    print("""
Two things to take away

  1. PRAGMA foreign_keys = ON, on every connection, every time. It is
     a property of the session, not of the database file, so setting
     it once does not stick.

  2. This is why 00_reset.py deletes the file rather than dropping
     tables. That orphan is not coming out any other way.

Clean up with:  python3 00_reset.py --rebuild""")


if __name__ == "__main__":
    main()
