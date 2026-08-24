"""
02_insert_a_venue.py  —  Add one record by hand, one statement at a time
HIST 8510  ·  Week 2  ·  Database Design

01_build_db.py inserts fifty-three venues in a loop, too fast to watch.
This script does it once, slowly, and prints every SQL statement before
it runs so you can read the SQL rather than the Python.

Nothing here is interactive. Run it and read down the output; the point
is the statements, not the typing.

Safe to run as many times as you like — step 1 removes the record a
previous run added.

Run it with:  python3 02_insert_a_venue.py
"""

import sqlite3

DB_FILE = "sc_guides.db"


# ---------------------------------------------------------------------
# A small helper so every step shows its SQL before running it.
# ---------------------------------------------------------------------
def run(cursor, sql, params=()):
    """Print a statement, run it, and return the cursor."""
    lines = [ln for ln in sql.strip("\n").rstrip().split("\n")]
    for ln in lines:
        print("    " + ln)
    if params:
        shown = ", ".join(repr(p) for p in params)
        print(f"\n    ?  =  {shown}")
    print()
    cursor.execute(sql, params)
    return cursor


def step(number, total, title, explanation=""):
    print("\n" + "-" * 66)
    print(f"STEP {number} of {total}  ·  {title}")
    print("-" * 66)
    if explanation:
        print(explanation.strip() + "\n")


def main():
    print("=" * 66)
    print("  Adding one venue by hand")
    print("=" * 66)
    print("""
Every statement below is printed before it runs. The ? marks are
placeholders — SQLite fills them in from the values listed underneath.
That is not a style choice, and step 5 explains why.""")

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Foreign key enforcement is OFF by default on every new connection.
    # 03_break_a_foreign_key.py shows what happens when you forget this.
    cursor.execute("PRAGMA foreign_keys = ON")

    # -----------------------------------------------------------------
    step(1, 5, "Start clean", """
Remove the venue a previous run added, so this script gives the same
result every time.

DELETE removes rows matching a WHERE condition. Without the WHERE it
would empty the whole table, which is worth knowing before you type it.

Order matters here, and it is the same rule as dropping tables. You
cannot delete a venue while rows in venue_type_link still point at it —
with foreign keys on, the database refuses. So the link rows go first.""")

    run(cursor, """
DELETE FROM venue_type_link
 WHERE venue_id IN (SELECT venue_id FROM venues WHERE title = ?);
""", ("The Blue Note",))
    print(f"  -> {cursor.rowcount} link row(s) deleted.\n")

    run(cursor, """
DELETE FROM venues
 WHERE title = ?;
""", ("The Blue Note",))
    print(f"  -> {cursor.rowcount} venue row(s) deleted.")
    print("     Try reversing those two statements and see what happens.")

    # -----------------------------------------------------------------
    step(2, 5, "Find the city this venue belongs to", """
Charleston is already in the cities table. We do not add it again — we
look up its id, because that id is what the venue row will point at.

SELECT asks for columns FROM a table WHERE a condition holds.""")

    run(cursor, """
SELECT city_id
  FROM cities
 WHERE city_name = ?
   AND state = ?;
""", ("Charleston", "SC"))
    city_id = cursor.fetchone()[0]
    print(f"  -> Charleston, SC is city_id {city_id}.")

    # -----------------------------------------------------------------
    step(3, 5, "Insert the venue", """
INSERT INTO names the table and the columns you are filling. VALUES
supplies one value per column, in the same order.

Columns you leave out get NULL, which is why street_address and
description can be omitted without error but title cannot — the schema
declares title as NOT NULL.""")

    run(cursor, """
INSERT INTO venues (title, year, source_id, street_address, city_id)
VALUES (?, ?, ?, ?, ?);
""", ("The Blue Note", 1978, "demo-1978-00001", "42 Meeting St.", city_id))

    venue_id = cursor.lastrowid
    print(f"  -> 1 row added. SQLite assigned venue_id {venue_id}.")
    print("     We never supplied a venue_id. INTEGER PRIMARY KEY means")
    print("     SQLite generates one, and lastrowid hands it back to us.")

    # -----------------------------------------------------------------
    step(4, 5, "Give it two types", """
This venue is both a bar and a cruising area. In the flat spreadsheet
that was one cell with a comma in it. Here it is two rows in the
junction table, each one pairing this venue with one category.

Same INSERT statement, run twice with different values.""")

    for label in ("Bars/Clubs", "Cruising Areas"):
        run(cursor, """
SELECT type_id FROM venue_types WHERE type_label = ?;
""", (label,))
        type_id = cursor.fetchone()[0]

        run(cursor, """
INSERT INTO venue_type_link (venue_id, type_id)
VALUES (?, ?);
""", (venue_id, type_id))
        print(f"  -> venue {venue_id} is now linked to type {type_id} ({label}).\n")

    conn.commit()
    print("  COMMIT — nothing above was permanent until this point.")

    # -----------------------------------------------------------------
    step(5, 5, "Read it back across all four tables", """
JOIN follows a foreign key. Each JOIN below says 'match rows in these
two tables wherever these two columns are equal', which is how the
venue, its city, and its categories get reassembled into one row.

GROUP_CONCAT collapses the two type rows back into one string for
display — note that we can always rebuild the flat view from the
normalized tables, but not the other way round.""")

    run(cursor, """
SELECT v.title,
       v.year,
       c.city_name,
       GROUP_CONCAT(t.type_label, ' + ') AS types
  FROM venues v
  JOIN cities c          ON v.city_id  = c.city_id
  JOIN venue_type_link l ON v.venue_id = l.venue_id
  JOIN venue_types t     ON l.type_id  = t.type_id
 WHERE v.venue_id = ?
 GROUP BY v.venue_id;
""", (venue_id,))

    title, year, city, types = cursor.fetchone()
    print(f"  -> {title} ({year}), {city} — {types}")

    conn.close()

    print("\n" + "=" * 66)
    print("""
Why the ? placeholders

  You could build the statement by pasting values into a string:

      "INSERT INTO venues (title) VALUES ('" + title + "')"

  Do not. A title containing an apostrophe — O'Farrell's, and this
  data is full of them — would end the string early and break the
  statement. Passing values separately lets SQLite handle the quoting,
  and it is the habit that keeps a web form from being able to rewrite
  your database later in the term.

Next:  python3 03_break_a_foreign_key.py""")


if __name__ == "__main__":
    main()
