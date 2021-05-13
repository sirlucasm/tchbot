import os
from tinydb import TinyDB, Query
from pathlib import Path

class Database:
    global db
    db = TinyDB('src/database/db.json')

    def exec():
        db = TinyDB('src/database/db.json', create_dirs=True)

    async def insert(tableName, data):
        table = db.table(tableName)
        table.insert(data)
