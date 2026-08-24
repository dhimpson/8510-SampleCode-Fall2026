"""
00_reset.py  —  Delete the database and start over
HIST 8510  ·  Week 2  ·  Database Design

Deletes sc_guides.db so the whole build can be run again from scratch.

Why delete the file instead of just dropping the tables? Because DROP TABLE
only removes tables the schema file currently knows about. Rename a table,
or remove one, and the old version quietly survives every rebuild. Deleting
the file is the only way to be certain you are starting from the same place
you started from last time.

You will also need this after running 03_break_a_foreign_key.py, which puts
a deliberately broken row into the database to show you what an unenforced
foreign key looks like. Once that orphan is in there, deleting the file is
the only way back out.

Run it with:       python3 00_reset.py
Reset and rebuild: python3 00_reset.py --rebuild
"""

import os
import sqlite3
import subprocess
import sys

DB_FILE = "sc_guides.db"


def main():
    rebuild = "--rebuild" in sys.argv

    print("=== Reset ===")

    if not os.path.exists(DB_FILE):
        print(f"\nNo database found ({DB_FILE}). Nothing to delete.")
    else:
        # Report what is in there before destroying it. Useful when you are
        # mid-class and not completely sure what state you left it in.
        print(f"\nFound {DB_FILE}. Current contents:")
        try:
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            tables = cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
            ).fetchall()
            if tables:
                for (name,) in tables:
                    count = cursor.execute(f"SELECT COUNT(*) FROM {name}").fetchone()[0]
                    print(f"  {name:<20} {count:>5} rows")
            else:
                print("  (no tables)")
            conn.close()
        except sqlite3.Error as e:
            print(f"  Could not read the database: {e}")

        os.remove(DB_FILE)
        print(f"\nDeleted {DB_FILE}")

    if rebuild:
        print("\nRebuilding...\n")
        subprocess.run([sys.executable, "01_build_db.py"], check=False)
        return

    print("\nTo build it again:")
    print("  python3 01_build_db.py            # create the tables and load the data")
    print("  python3 02_insert_a_venue.py      # add one record, statement by statement")
    print("  python3 03_break_a_foreign_key.py # watch a bad insert succeed silently")
    print("\nOr do both at once next time with:  python3 00_reset.py --rebuild")


if __name__ == "__main__":
    main()
