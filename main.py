from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from typing import List

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Allowed fields for field-specific queries
ALLOWED_FIELDS = {"title", "creators", "publication", "tags", "abstract"}

# Sortable fields from base table
SORTABLE_FIELDS = {"title", "creators", "publication", "date"}

# Map fields to FTS5 column indexes for highlight()
FTS_COLUMN_INDEX = {
    "title": 0,
    "creators": 1,
    "publication": 2,
    "tags": 3,
    "abstract": 4,
}

def build_fts_query(raw_query: str) -> str:
    tokens = raw_query.split()
    parsed_tokens = []

    for token in tokens:
        if token.upper() in {"AND", "OR", "NOT"}:
            parsed_tokens.append(token.upper())
        elif ":" in token:
            field, value = token.split(":", 1)
            if field in ALLOWED_FIELDS:
                if not value.endswith("*"):
                    value += "*"
                parsed_tokens.append(f"{field}:{value}")
        else:
            if not token.endswith("*"):
                token += "*"
            parsed_tokens.append(token)

    return " ".join(parsed_tokens)

def search_db(raw_query: str, page: int, limit: int, sort: str = None, order: str = "asc"):
    offset = (page - 1) * limit
    conn = sqlite3.connect("zotero.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    fts_query = build_fts_query(raw_query)

    # Validate sort field
    sort_clause = ""
    if sort in SORTABLE_FIELDS and order.lower() in {"asc", "desc"}:
        sort_clause = f"ORDER BY zotero_items.{sort} {order.upper()}"

    # Get total count
    cursor.execute("""
        SELECT COUNT(*) FROM zotero_items_fts
        WHERE zotero_items_fts MATCH ?
    """, (fts_query,))
    total = cursor.fetchone()[0]

    # Paginated + sorted results
    cursor.execute(f"""
        SELECT 
            zotero_items.id,
            highlight(zotero_items_fts, 0, '<b>', '</b>') AS title,
            highlight(zotero_items_fts, 1, '<b>', '</b>') AS creators,
            highlight(zotero_items_fts, 2, '<b>', '</b>') AS publication,
            zotero_items.volume,
            zotero_items.issue,
            zotero_items.pages,
            zotero_items.date,
            zotero_items.DOI,
            zotero_items.url,
            highlight(zotero_items_fts, 3, '<b>', '</b>') AS tags,
            highlight(zotero_items_fts, 4, '<b>', '</b>') AS abstract,
            zotero_items.authortype,
            zotero_items.itemtype
        FROM zotero_items_fts
        JOIN zotero_items ON zotero_items_fts.rowid = zotero_items.id
        WHERE zotero_items_fts MATCH ?
        {sort_clause}
        LIMIT ? OFFSET ?
    """, (fts_query, limit, offset))

    results = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "results": results
    }

@app.get("/search")
def search(
    q: str = Query(..., min_length=1),
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100),
    sort: str = Query(None),
    order: str = Query("asc")
):
    return search_db(q, page, limit, sort, order)