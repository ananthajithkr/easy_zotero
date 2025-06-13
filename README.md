# easy zotero

an easy, google-like wrapper for zotero.

## the components perform these tasks

Backend

1. fetch json data (all items and fields) from zotero (group or individual libraries) using API and pyzotero
2. flatten the json data
3. define a schema for a sql table and a sqlite fs5 virtual table (sortable sql table and faster fs5 version)
4. write the json data into the sqlite database
5. create an API so that a frontend can query the database (supports pagination and highlighting search terms)

Frontend

1. HTML and CSS to style the page
2. Javascript queries the API and tabulates the result

## Features

1. fuzzy search
2. fast response: all processing done on the backend
3. light on the browser: frontend queries the database using a custom API
4. searches the whole of zotero data. NOT limited to author, title, publication.
5. Custom group/personal library can be configured as the database

## Requirements

Python3, pyzotero, sqlite3, uvicorn, zotero API key

## Deployment

1. Run python scripts to generate the database.
2. Initiate a server on localhost


acknowledgment: as an example, this project uses [Urava Kerala Bibliography](https://www.zotero.org/groups/283088/urava_kerala_bibliography/library)

