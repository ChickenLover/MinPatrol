import os
import json
import importlib

from db_comp import *

def add_control(control_id, status):
    statuses = dict(enumerate(
        ["STATUS_COMPLIANT",
        "STATUS_NOT_COMPLIANT",
        "STATUS_NOT_APPLICABLE",
        "STATUS_ERROR",
        "STATUS_EXCEPTION"], 1))

    db = get_db()
    c = db.cursor()
    c.execute('SELECT * FROM controls WHERE id=?', str(control_id))
    complaint_data = c.execute('SELECT * FROM controls WHERE id=?', str(control_id)).fetchone()

    c.execute('\
            INSERT INTO scandata(id, description, status)\
            VALUES(?,?,?)', tuple(list(complaint_data) + [statuses[status]])
    )
    db.commit()
    db.close()

def main():
    for script_name in [f for f in os.listdir("./scripts") if f[-3:] == '.py']:
        script = importlib.import_module("scripts." + script_name[:-3])
        add_control(0, script.main())

if __name__=="__main__":
    initialize_tables()
    main()
