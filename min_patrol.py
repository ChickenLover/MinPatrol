import socket
import json

from paramiko import SSHClient, AutoAddPolicy
from paramiko.ssh_exception import *

class TransportError(Exception):
    pass

class TransportIOError(TransportError):
    pass

class TransportConnectionError(TransportError):
    pass

class UnknownTransport(TransportError):
    pass

class SSHTransport():
    def __init__(self, host, port_, login, password):
        self.client = SSHClient()
        self.client.set_missing_host_key_policy(AutoAddPolicy())
        try:
            self.client.connect(hostname=host, username=login, password=password, port=port_)
        except BadHostKeyException:
            raise TransportConnectionError("Can't resolve host key")
        except 	AuthenticationException:
            raise TransportConnectionError("Can't login on {} by pass: {}".format(login, password))
        except SSHException:
            raise TransportConnectionError("Some socket exception")
        except socket.error:
            raise TransportConnectionError("Can't connect to {} port on {}".format(port_, host))

    def exec(self, command):
        try:
            return self.client.exec_command(command)
        except SSHException:
            raise TransportConnectionError("SSHException")

    def get_file(self, path):
        try:
            return self.client.open_sftp().open(path).read().decode()
        except SSHException:
            raise TransportConnectionError
        except IOError:
            raise TransportIOError("Can't open file by path {}".format(path))

def get_transport(transport_name, host=None, port=None,login=None, password=None):
    available_transports = {'ssh':SSHTransport}
    with open("./env.json") as f: config = json.load(f)
    
    transport_name = transport_name.lower()
    transport = available_transports.get(transport_name, None)
    if not transport:
        raise UnknownTransport('No such transport')

    host = config['host'] if not host else host
    transport_data = config['transports'][transport_name]
    port = transport_data['port'] if not port else port
    login = transport_data['login'] if not login else login
    password = transport_data['password'] if not password else password

    return transport(host, port, login, password)
