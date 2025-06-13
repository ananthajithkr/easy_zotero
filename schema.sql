-- Base table
CREATE TABLE IF NOT EXISTS zotero_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    authortype TEXT,
    itemtype TEXT,
    title TEXT,
    creators TEXT,
    publication TEXT,
    volume TEXT,
    issue TEXT,
    pages TEXT,
    date TEXT,
    DOI TEXT,
    url TEXT,
    tags TEXT,
    abstract TEXT
);

-- FTS5 table for full-text search
CREATE VIRTUAL TABLE IF NOT EXISTS zotero_items_fts
USING fts5(
    title,
    creators,
    publication,
    tags,
    abstract,
    content='zotero_items',
    content_rowid='id'
);