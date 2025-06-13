import sqlite3

# Connect to the database
conn = sqlite3.connect("zotero.db")
cursor = conn.cursor()

# Fetch and print the first 5 rows from the base table
cursor.execute("SELECT id, title, creators, publication, date FROM zotero_items LIMIT 5;")
rows = cursor.fetchall()

print("Sample records from zotero_items:\n")
for row in rows:
    print(f"ID: {row[0]}")
    print(f"Title: {row[1]}")
    print(f"Creators: {row[2]}")
    print(f"Publication: {row[3]}")
    print(f"Date: {row[4]}")
    print("-" * 40)

conn.close()