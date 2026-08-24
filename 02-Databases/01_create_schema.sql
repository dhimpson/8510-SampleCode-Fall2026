-- =====================================================================
-- 01_create_schema.sql
-- HIST 8510  ·  Week 2  ·  Database Design
--
-- Four tables for a slice of Bob Damron's Address Book, South Carolina.
--
-- Read this file top to bottom. It is not just setup code. Every line
-- below is a decision about how these guidebooks get turned into
-- evidence, and the comments are the argument for each decision.
--
-- You can run this whole file with 01_build_db.py, or you can open it
-- in DBcode and run one statement at a time to watch the tables appear.
-- =====================================================================


-- Start clean. Dropping in reverse order of creation matters: you cannot
-- drop a table another table still points at.
--
-- Note that these DROP statements only remove tables THIS file knows
-- about. If you rename a table later, the old one lingers. That is why
-- 00_reset.py deletes the database file outright instead of relying on
-- these lines.
DROP TABLE IF EXISTS venue_type_link;
DROP TABLE IF EXISTS venues;
DROP TABLE IF EXISTS venue_types;
DROP TABLE IF EXISTS cities;


-- ---------------------------------------------------------------------
-- cities
-- ---------------------------------------------------------------------
-- In the flat spreadsheet, "Charleston" is typed out on every single
-- listing. That repetition is the tell: a value that repeats down a
-- column is usually an entity you have not pulled out yet.
--
-- Storing it once means a typo can be fixed in one place, and it means
-- "Charleston" is now a thing the database knows about rather than a
-- string that happens to recur.
CREATE TABLE cities (
    city_id     INTEGER PRIMARY KEY,   -- surrogate key: SQLite assigns it
    city_name   TEXT NOT NULL,
    state       TEXT NOT NULL,

    -- Stops us from ending up with two Charlestons. Constraints are how
    -- you write your assumptions down where the database can enforce them.
    UNIQUE (city_name, state)
);


-- ---------------------------------------------------------------------
-- venue_types
-- ---------------------------------------------------------------------
-- The categories Damron used, kept EXACTLY as printed.
--
-- You will notice this table contains "Bars", "Bars/Clubs", "Bars &
-- Nightclubs", and "Nightclubs". It also contains both "Cruising Areas"
-- and "Cruisy Areas". Those look like errors waiting to be cleaned up.
--
-- They are not errors. The guides ran from 1965 to 2003 and their own
-- vocabulary shifted over that time. If we merge them, counting gets
-- easier and we quietly erase the fact that the category changed. If we
-- keep them apart, we preserve the change and make counting harder.
--
-- There is no correct answer. There is only a decision, and this schema
-- is where you record which one you made. (Rawson and Munoz, "Against
-- Cleaning.")
CREATE TABLE venue_types (
    type_id     INTEGER PRIMARY KEY,
    type_label  TEXT NOT NULL UNIQUE
);


-- ---------------------------------------------------------------------
-- venues
-- ---------------------------------------------------------------------
-- THE BIG DECISION IN THIS FILE.
--
-- One row here is one LISTING: one venue, in one guide year. So
-- Bushwacker's Pub, which appears in eight editions, is eight rows.
--
-- The alternative is to treat Bushwacker's as one venue with eight
-- listings attached, which would mean a fifth table. That version is
-- truer to the sources, because Bushwacker's is one bar and not eight
-- bars. It also makes "how did this venue change over time?" a much more
-- natural question to ask.
--
-- We are building the simpler version because it fits in one class. Know
-- that it costs you something: to ask about a single venue across time
-- you now have to match on title and city, and titles in this data are
-- not reliable. The full file contains both "Beach at 82nd Ave." and
-- "Beach at 82nd Ave" as separate places, differing by one period.
--
-- That is also the reason venue_id is a surrogate key. There is no field
-- in these guidebooks stable enough to identify a place across editions.
CREATE TABLE venues (
    venue_id        INTEGER PRIMARY KEY,

    title           TEXT NOT NULL,     -- required: no name, no record
    year            INTEGER,           -- INTEGER, so it sorts and compares
                                       -- as a number. See the note below
                                       -- about what SQLite will let you
                                       -- put here anyway.
    source_id       TEXT,              -- e.g. d-1989-01337. Not our key,
                                       -- but it is the path back to the
                                       -- printed page. Always keep one.
    street_address  TEXT,              -- often missing; nullable on purpose
    description     TEXT,              -- the guide's own annotation

    city_id         INTEGER NOT NULL,  -- the foreign key sits on the MANY
                                       -- side. One city has many venues;
                                       -- one venue sits in one city.

    FOREIGN KEY (city_id) REFERENCES cities (city_id)
);


-- ---------------------------------------------------------------------
-- venue_type_link   (the junction table)
-- ---------------------------------------------------------------------
-- One venue can be several things at once. One category describes many
-- venues. That is a many-to-many relationship, and neither table can
-- hold the foreign key for it. There is nowhere to put it.
--
-- So the relationship becomes a table of its own. Two foreign keys, one
-- row per pairing, and nothing else.
--
-- In the flat sheet, Adult World in 1989 was one cell reading
--     "Book Store,Cruising Areas,Erotic Shop"
-- Here it is three rows. The comma ordering disappears, which is correct,
-- because it never meant anything in the first place.
CREATE TABLE venue_type_link (
    venue_id    INTEGER NOT NULL,
    type_id     INTEGER NOT NULL,

    -- The primary key is the PAIR. This is what stops the same venue
    -- from being tagged "Bars" twice, and it is a very common shape for
    -- a junction table.
    PRIMARY KEY (venue_id, type_id),

    FOREIGN KEY (venue_id) REFERENCES venues (venue_id),
    FOREIGN KEY (type_id)  REFERENCES venue_types (type_id)
);


-- =====================================================================
-- TWO THINGS SQLITE WILL LET YOU GET AWAY WITH
--
-- 1. Declared types are suggestions. Writing `year INTEGER` above does
--    not stop SQLite from storing the text 'c. 1985' in that column. It
--    will accept it without complaint, and then `WHERE year > 1980` will
--    quietly not match that row. Other databases refuse. SQLite does not.
--
-- 2. Foreign keys are not enforced unless you ask. Every FOREIGN KEY
--    line above is inert by default. You have to run
--
--        PRAGMA foreign_keys = ON;
--
--    on EVERY connection, every time. It is a property of the session,
--    not of the file, so turning it on once does not stick.
--
--    01_build_db.py sets it. If you write your own script and forget,
--    you can insert a venue pointing at a city that does not exist and
--    nothing will ever tell you. Run 03_break_a_foreign_key.py to
--    watch it happen.
-- =====================================================================
