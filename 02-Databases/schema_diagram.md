# Schema diagram

The four tables and how they connect. This is the convention to copy for
documenting your own database.

Mermaid renders on GitHub automatically, so a diagram written this way lives
in your repository as text you can edit rather than an image you have to
regenerate every time the schema changes.

```mermaid
erDiagram
    cities ||--o{ venues : "one city has many venues"
    venues ||--o{ venue_type_link : ""
    venue_types ||--o{ venue_type_link : ""

    cities {
        INTEGER city_id PK
        TEXT    city_name
        TEXT    state
    }

    venue_types {
        INTEGER type_id PK
        TEXT    type_label "the guide's own wording, unmerged"
    }

    venues {
        INTEGER venue_id PK
        TEXT    title
        INTEGER year "one row per venue per guide year"
        TEXT    source_id "d-1989-01337, the path back to the page"
        TEXT    street_address
        TEXT    description
        INTEGER city_id FK
    }

    venue_type_link {
        INTEGER venue_id PK-FK
        INTEGER type_id PK-FK
    }
```

## How to read it

`cities ||--o{ venues` is a one-to-many. One city, many venues. The crow's
foot (the `o{` end) sits on the many side, and that is also the side carrying
the foreign key.

`venue_type_link` is the junction table. It has two one-to-many relationships
pointing into it, one from each side, and together those make the many-to-many
between venues and types. A venue can be several things at once; a category
describes many venues. Neither table could hold that on its own.

Note that `venue_type_link` has no id of its own. Its primary key is the pair
of foreign keys, which is what stops the same venue being tagged with the same
category twice.

## The thing this diagram does not show

One row in `venues` is one *listing*, meaning one venue in one guide year.
Bushwacker's Pub is eight rows here, not one. A diagram cannot tell you that,
which is why your README has to.
