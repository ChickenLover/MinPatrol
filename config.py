
import json
with open("./env.json") as f: _config = json.load(f)

def get_system_host():
    global _config
    return _config['host']

def get_transport_config(transport_name):
    global _config
    return _config['transports'].get(transport_name.lower(), None)
