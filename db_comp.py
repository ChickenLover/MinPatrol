import json

import sqlite3

DBNAME = "data.db"

def get_db():
    return sqlite3.connect(DBNAME)

def initialize_tables():
    db = get_db()
    c = db.cursor()
    c.execute('\
            CREATE TABLE IF NOT EXISTS controls(\
            id INTEGER PRIMARY KEY,\
            description TEXT)')

    c.execute('\
            CREATE TABLE IF NOT EXISTS\
            scandata(\
            id INTEGER PRIMARY KEY,\
            description,\
            status\
            )')
    db.commit()

    with open("controls.json") as f:
        controls = json.load(f)

    for complaint_record in controls:
        c.execute('\
            INSERT INTO controls(id, description)\
            VALUES (?,?)', tuple(complaint_record))
        db.commit()
    db.close()
