# urava_prod

production repo which contains all code for building urava front end and instructions to run it.

Directory layout

---

urava/
├── main.py               # Starts FastAPI app
├── fetch_zotero.py       # Fetch data from Zotero API
├── db/
│   ├── init_db.py        # Create tables, schema
│   ├── schema.sql        # Schema (with FTS5)
│   └── load_data.py      # Load JSON into SQLite
├── search/
│   └── query.py          # Search logic using FTS5
├── api/
│   └── endpoints.py      # FastAPI routes
├── static/
│   └── index.html        # Your frontend UI
└── zotero_items.json     # Raw data (optional, for loading)

---
