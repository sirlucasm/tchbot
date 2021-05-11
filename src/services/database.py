import os
from tinydb import TinyDB, Query
from pathlib import Path

class Database:
    global db
    db = TinyDB('src/database/db.json')

    def exec():
        db = TinyDB('src/database/db.json', create_dirs=True)

    def insert(tableName, data):
        table = db.table('users')
        table.insert(data)
