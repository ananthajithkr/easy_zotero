# easy zotero

an easy, google-like wrapper for zotero. can be configured for any group library.

## the components perform these tasks

Backend

1. fetch json data (all items and fields) from zotero (group or individual libraries) using API and pyzotero
2. flatten the json data
3. define a schema for a sql table and a sqlite fs5 virtual table (sortable sql base table and faster fs5 version)
4. write the json data into the sqlite database
5. create an API so that a frontend can query the database (supports pagination and highlighting search terms)

Frontend

1. HTML and CSS to style the page and provide a search interface
2. Javascript queries the API and tabulates the result

## Features

1. fuzzy search
2. fast response: all processing done on the backend
3. sortable table
4. field-specific seaerch
5. URL updates to reflect current search; can be shared and/or bookmarked
6. light on the browser: frontend queries the database using a custom API
7. searches the whole of zotero data. NOT limited to author, title, publication.
8. Custom group/personal library can be configured as the database
9. modularity: each process is a module.

## Requirements

python3, pyzotero, sqlite3, uvicorn, zotero API key

## Deployment

1. Insert your API Key and Group ID into fetch_zotero.py
2. Run python scripts to generate the database (fetch>flatten>schema>execute_schema>insert_data>ensure_and_rebuild>main)
3. Run uvicorn and a python server on your local machine (API listens on port 8000)
4. Point your browser to localhost (port 5500)

## Acknowledgements
pyzotero for the python client, zotero for the API


