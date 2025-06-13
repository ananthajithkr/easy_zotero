import json

def flatten_creators(creators):
    names = []
    types = set()
    for c in creators:
        t = c.get("creatorType", "")
        types.add(t)
        last = c.get("lastName", "").strip()
        first = c.get("firstName", "").strip()
        if last or first:
            names.append(f"{last}, {first}".strip(", "))
    return "; ".join(names), "; ".join(types)

def flatten_item(item):
    data = item.get("data", {})
    creators_raw = data.get("creators", [])
    creators_str, authortypes = flatten_creators(creators_raw)

    return {
        "authortype": authortypes,
        "itemtype": data.get("itemType", ""),
        "title": data.get("title", ""),
        "creators": creators_str,
        "publication": data.get("publicationTitle", ""),
        "volume": data.get("volume", ""),
        "issue": data.get("issue", ""),
        "pages": data.get("pages", ""),
        "date": data.get("date", ""),
        "DOI": data.get("DOI", ""),
        "url": data.get("url") or item.get("links", {}).get("alternate", {}).get("href", ""),
        "tags": "; ".join(tag.get("tag", "") for tag in data.get("tags", [])),
        "abstract": data.get("abstractNote", "")
    }

# Load zotero_items.json
with open("zotero_items.json", "r", encoding="utf-8") as f:
    items = json.load(f)

# Flatten
flattened = [flatten_item(item) for item in items]

# Save to flattened_zotero.json
with open("flattened_zotero.json", "w", encoding="utf-8") as f:
    json.dump(flattened, f, indent=2, ensure_ascii=False)

print(f"Flattened {len(flattened)} items into flattened_zotero.json")