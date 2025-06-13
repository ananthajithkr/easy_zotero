import time
import json
from pyzotero import zotero

# === CONFIG ===
API_KEY = 'insert-your-api-key'
GROUP_ID = 'insert-group-id'
LIBRARY_TYPE = 'group'
BATCH_SIZE = 100
WAIT_TIME = 1  # seconds
OUTPUT_FILE = 'zotero_items.json'

def fetch_all_items():
    zot = zotero.Zotero(GROUP_ID, LIBRARY_TYPE, API_KEY)
    all_items = []
    start = 0

    while True:
        print(f'Fetching items {start} to {start + BATCH_SIZE}...')
        items = zot.items(limit=BATCH_SIZE, start=start)
        all_items.extend(items)

        if len(items) < BATCH_SIZE:
            print('Final batch received. Done.')
            break

        start += BATCH_SIZE
        time.sleep(WAIT_TIME)

    print(f'Total items fetched: {len(all_items)}')
    return all_items

def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f'Saved data to {filename}')

if __name__ == '__main__':
    items = fetch_all_items()
    save_to_json(items, OUTPUT_FILE)
