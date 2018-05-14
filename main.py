import os
import importlib
import time

from db_comp import *
from reporting import make_report


def add_control(control_id, status):
    db = get_db()
    db.cursor().execute('\
            INSERT OR IGNORE INTO scandata(id, status)\
            VALUES(?,?)', (control_id, statuses[status]))
    db.commit()
    db.close()


def main():
    initialize_tables()
    start_time = time.time()
    for module_name in filter(lambda f: f.endswith('.py'), os.listdir("./scripts")):
        script = importlib.import_module("." + module_name[:-3], package='scripts')
        add_control(int(module_name[:3]), script.main())
    time_passed = time.time() - start_time
    make_report(time_passed)


if __name__ == "__main__":
    main()
