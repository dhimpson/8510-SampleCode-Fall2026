-- =====================================================================
-- schema.sql
-- HIST 8510  ·  Week 2 mini-assignment
--
-- YOUR NAME:
-- YOUR SOURCES (one line — what are they, roughly how many, what years):
--
--
-- Write your schema here. Look at 01_create_schema.sql in the week folder
-- for a worked example, but do not just rename its tables. Your sources
-- are not Damron's guidebooks and they will not want the same shape.
--
-- Requirements for Wednesday:
--   · at least three tables
--   · at least one genuine many-to-many, modeled with a junction table
--   · comments explaining WHY, not just what
--
-- Run it with build_db.py, or open it in DBcode and run one statement
-- at a time.
-- =====================================================================


-- Start clean, in reverse order of creation. You cannot drop a table
-- that another table still points at.
-- DROP TABLE IF EXISTS ...
-- DROP TABLE IF EXISTS ...


-- ---------------------------------------------------------------------
-- Table 1 — probably your lookup or "one" side
-- ---------------------------------------------------------------------
-- Ask yourself: what value is repeated over and over in my flat notes?
-- That repetition usually means an entity you have not pulled out yet.
--
-- CREATE TABLE ... (
--     ..._id    INTEGER PRIMARY KEY,
--     ...
-- );


-- ---------------------------------------------------------------------
-- Table 2 — your central table, the thing you have the most rows of
-- ---------------------------------------------------------------------
-- Two things to decide here, and to write down in a comment:
--
--   1. What is ONE ROW? Be exact. "One petition" and "one signature on a
--      petition" are different databases.
--
--   2. Is there a field in your sources stable enough to be a natural
--      key? Usually not. Use a surrogate integer and keep the source's
--      own identifier as an ordinary column so you can get back to the
--      document.
--
-- CREATE TABLE ... (
--     ..._id    INTEGER PRIMARY KEY,
--     ...       TEXT NOT NULL,
--     ..._id    INTEGER NOT NULL,      -- foreign key goes on the many side
--     FOREIGN KEY (..._id) REFERENCES ... (..._id)
-- );


-- ---------------------------------------------------------------------
-- Table 3 — the junction table
-- ---------------------------------------------------------------------
-- This is the one people skip, and it is the one Wednesday is for.
--
-- You need it whenever a thing can have several of something AND that
-- something describes several things. Multiple authors on a document.
-- Multiple topics on a petition. Multiple people at an event.
--
-- If you find yourself wanting a column called topic_1, topic_2,
-- topic_3, or a single column holding "war, pensions, land" with commas
-- in it, that is a many-to-many asking for a junction table.
--
-- CREATE TABLE ..._link (
--     ..._id    INTEGER NOT NULL,
--     ..._id    INTEGER NOT NULL,
--     PRIMARY KEY (..._id, ..._id),
--     FOREIGN KEY (..._id) REFERENCES ... (..._id),
--     FOREIGN KEY (..._id) REFERENCES ... (..._id)
-- );


-- =====================================================================
-- Remember: PRAGMA foreign_keys = ON has to be set on every connection.
-- The FOREIGN KEY lines above do nothing without it. build_db.py sets it.
-- =====================================================================
