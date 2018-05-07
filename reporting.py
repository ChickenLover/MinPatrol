import time
import json
from collections import Counter

from jinja2 import Environment, FileSystemLoader, select_autoescape
from weasyprint import HTML, CSS

from db_comp import get_db, statuses

def make_report(scan_time):
    #Get columns with names
    db = get_db()
    cursor = db.execute('\
        SELECT * FROM scandata AS t1 \
        INNER JOIN controls AS t2\
        ON t1.id=t2.id')
    columns_names = map(lambda n: n[0], cursor.description)
    compliances = [dict(zip(columns_names, compliance)) for compliance in cursor.fetchall()]

    #Count statuses occurances, set 0 if none, rename keys
    checks_counts = dict(Counter([c['status'] for c in compliances]))
    checks_counts.update({status:0 for status in statuses.values() if status not in checks_counts})
    checks_counts = {'{}_checks'.format(status):count for status, count in checks_counts.items()}

    #Get transports and fill transports data
    transports_used = set([c['transport'] for c in compliances])
    with open("./env.json") as f: env_config = json.load(f)
    transports_data = {trans: env_config['transports'][trans.lower()] for trans in transports_used}

    #Form render data dict
    render_data = {
        'scan_date':time.asctime(),
        'scan_time':scan_time,
        'system_host':env_config['host'],
        'total_checks':len(compliances),
        'transports':transports_data,
        'comp_data':compliances
    }
    render_data.update(checks_counts)
    
    #Render pdf from HTML
    env = Environment(
        loader=FileSystemLoader('templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    rendered_template = env.get_template('index.html').render(**render_data)
    styles = [CSS(filename='./templates/style.css')]
    HTML(string = rendered_template).write_pdf('sample_report.pdf', stylesheets=styles)   
