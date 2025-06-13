import sqlite3
import json

# Load and execute schema.sql
with open("schema.sql", "r", encoding="utf-8") as f:
    schema_sql = f.read()

conn = sqlite3.connect("zotero.db")
cursor = conn.cursor()
cursor.executescript(schema_sql)
print("schema.sql executed successfully.")

# Load flattened JSON data
with open("flattened_zotero.json", "r", encoding="utf-8") as f:
    items = json.load(f)

# Insert into base table
insert_query = """
    INSERT INTO zotero_items (
        authortype, itemtype, title, creators, publication,
        volume, issue, pages, date, DOI, url, tags, abstract
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

for item in items:
    cursor.execute(insert_query, (
        item.get("authortype", ""),
        item.get("itemtype", ""),
        item.get("title", ""),
        item.get("creators", ""),
        item.get("publication", ""),
        item.get("volume", ""),
        item.get("issue", ""),
        item.get("pages", ""),
        item.get("date", ""),
        item.get("DOI", ""),
        item.get("url", ""),
        item.get("tags", ""),
        item.get("abstract", "")
    ))

conn.commit()
conn.close()

print(f"Inserted {len(items)} items into zotero_items.")