import sqlite3

DB_PATH = "zotero.db"

def ensure_and_rebuild_fts():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check if FTS table exists
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='zotero_items_fts';
    """)
    exists = cursor.fetchone()

    # Create the FTS5 table if it doesn't exist
    if not exists:
        print("FTS5 table not found. Creating...")
        cursor.execute("""
            CREATE VIRTUAL TABLE zotero_items_fts USING fts5(
                title,
                creators,
                publication,
                tags,
                abstract,
                content='zotero_items',
                content_rowid='id'
            );
        """)
        conn.commit()
        print("FTS5 table created.")

    # Rebuild the FTS5 index from base table
    try:
        print("Rebuilding FTS5 index...")
        cursor.execute("INSERT INTO zotero_items_fts(zotero_items_fts) VALUES('rebuild');")
        conn.commit()
        print("FTS5 index rebuilt successfully.")
    except sqlite3.Error as e:
        print("Failed to rebuild FTS5 index:", e)
    finally:
        conn.close()

if __name__ == "__main__":
    ensure_and_rebuild_fts()