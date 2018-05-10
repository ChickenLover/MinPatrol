import time
from collections import Counter

from jinja2 import Environment, FileSystemLoader, select_autoescape
from weasyprint import HTML, CSS

from config import get_system_host, get_transport_config
from db_comp import get_db, statuses


def make_report(scan_time):
    # Get columns with names
    db = get_db()
    cursor = db.execute('\
        SELECT * FROM scandata AS t1 \
        INNER JOIN controls AS t2\
        ON t1.id=t2.id')
    columns_names = [n[0] for n in cursor.description]
    compliances = [dict(zip(columns_names, comp)) for comp in cursor.fetchall()]

    # Count statuses occurances, set 0 if none, rename keys
    checks_counts = dict(Counter([c['status'] for c in compliances]))
    checks_counts.update({s: 0 for s in statuses.values() if s not in checks_counts})
    checks_counts = {'{}_checks'.format(s): c for s, c in checks_counts.items()}

    # Get transports and fill transports data, removing password
    transports_used = set([c['transport'] for c in compliances])
    transports_data = dict()
    for trans in transports_used:
        trans_conf = get_transport_config(trans)
        trans_conf.pop('password')
        transports_data[trans] = trans_conf 
    
    # Form render data dict
    scan_hours = scan_time // 3600
    scan_minutes = scan_time % 3600 // 60
    scan_seconds = scan_time % 60
    scan_time_str = f"{scan_hours}h {scan_minutes}m {scan_seconds:.2f}s"
    render_data = {
        'scan_date': time.asctime(),
        'scan_time': scan_time_str,
        'system_host': get_system_host(),
        'total_checks': len(compliances),
        'transports': transports_data,
        'comp_data': compliances
    }
    render_data.update(checks_counts)
    
    # Render pdf from HTML
    env = Environment(
        loader=FileSystemLoader('templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    rendered_template = env.get_template('index.html').render(**render_data)
    styles = [CSS(filename='./templates/style.css')]
    HTML(string=rendered_template).write_pdf('sample_report.pdf', stylesheets=styles)
