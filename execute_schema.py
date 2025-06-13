import sqlite3

with open("schema.sql", "r", encoding="utf-8") as f:
    schema_sql = f.read()

conn = sqlite3.connect("zotero.db")
cursor = conn.cursor()
cursor.executescript(schema_sql)
conn.commit()
conn.close()

print("schema.sql executed successfully.")