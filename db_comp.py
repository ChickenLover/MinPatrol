import json

import sqlite3

DBNAME = "data.db"
statuses = dict(enumerate(
    ["STATUS_COMPLIANT",
    "STATUS_NOT_COMPLIANT",
    "STATUS_NOT_APPLICABLE",
    "STATUS_ERROR",
    "STATUS_EXCEPTION"], 1))

def get_db():
    return sqlite3.connect(DBNAME)

def initialize_tables():
    db = get_db()
    c = db.cursor()
    c.execute('\
            CREATE TABLE IF NOT EXISTS controls(\
            id INTEGER PRIMARY KEY,\
            title TEXT,\
            description TEXT,\
            requirements TEXT,\
            transport TEXT)')

    c.execute('\
            CREATE TABLE IF NOT EXISTS\
            scandata(\
            id INTEGER PRIMARY KEY,\
            status\
            )')
    db.commit()

    with open("controls.json") as f:
        controls = json.load(f)

    for compliance_record in controls:
        c.execute('\
            INSERT OR IGNORE INTO controls(id, title, description, requirements, transport)\
            VALUES (?,?,?,?,?)', tuple(compliance_record))
        db.commit()
    db.close()
