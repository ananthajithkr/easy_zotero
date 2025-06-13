import sqlite3

# Connect to the SQLite DB
conn = sqlite3.connect("zotero.db")
cursor = conn.cursor()

# 1. Check how many records are in the base table
cursor.execute("SELECT COUNT(*) FROM zotero_items")
base_count = cursor.fetchone()[0]
print("Base table record count:", base_count)

# 2. Check how many records are in the FTS5 table
cursor.execute("SELECT COUNT(*) FROM zotero_items_fts")
fts_count = cursor.fetchone()[0]
print("FTS5 table record count:", fts_count)

# 3. If FTS5 is empty but base has data, rebuild FTS5 index
if base_count > 0 and fts_count == 0:
    print("Rebuilding FTS5 index...")
    cursor.execute("INSERT INTO zotero_items_fts(zotero_items_fts) VALUES('rebuild');")
    conn.commit()
    print("FTS5 index rebuilt.")

# 4. Test a search
query = "Jameela"
print(f"\nSearching FTS for: '{query}'")
cursor.execute("""
    SELECT zotero_items.id, zotero_items.title, zotero_items.creators,
           zotero_items.publication, zotero_items.date
    FROM zotero_items
    JOIN zotero_items_fts ON zotero_items.id = zotero_items_fts.rowid
    WHERE zotero_items_fts MATCH ?
    LIMIT 5;
""", (query,))
results = cursor.fetchall()

if results:
    for row in results:
        print(row)
else:
    print("No results found.")

# Done
conn.close()