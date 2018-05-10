import socket

from paramiko import SSHClient, AutoAddPolicy
from paramiko.ssh_exception import *
import pymysql
from pymysql.err import *

from config import get_transport_config, get_system_host


class TransportError(Exception):
    pass


class TransportIOError(TransportError):
    pass


class TransportConnectionError(TransportError):
    pass


class UnknownTransport(TransportError):
    def __init___(self, dErrorArguments):
        TransportError.__init__(self, "UnknownTransport {0}".format(dErrArguments))
        self.dErrorArguments = dErrorArguements


class MySQLError(TransportError):
    pass


class SSHTransport():
    def __init__(self, host, port, login, password):
        self.client = SSHClient()
        self.client.set_missing_host_key_policy(AutoAddPolicy())
        try:
            self.client.connect(hostname=host,
                                username=login,
                                password=password,
                                port=port)
        except BadHostKeyException:
            raise TransportConnectionError("Can't resolve host key")
        except AuthenticationException:
            raise TransportConnectionError("Can't login on \
                                            {} by pass: {}".format(login, password))
        except SSHException:
            raise TransportConnectionError("Some socket exception")
        except socket.error:
            raise TransportConnectionError("Can't connect to \
                                            {} port on {}".format(port, host))

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


class SQLTransport():
    def __init__(self, hostname, port, login, password):
        db = 'transport'
        try:
            self.connection = pymysql.connect(host=hostname, user=login,
                                              port=port, password=password,
                                              db=db, charset='utf8',
                                              cursorclass=pymysql.cursors.DictCursor,
                                              unix_socket=False)
        except InternalError:
            raise TransportConnectionError("Unknown database {}".format(db))
        except OperationalError:
            raise TransportConnectionError("Can't connect\
                                           to MySQL server on \
                                           '{}'@'{}' with\
                                           given password".format(login, hostname))
        except ProgrammingError:
            raise TransportConnectionError("Unable to connect\
                                           to port {} on {}".format(port, hostname))

    def sqlexec(self, quary):
        with self.connection.cursor() as cursor:
            cursor.execute(quary)
            self.connection.commit()
            return cursor.fetchall()

    def __del__(self):
        self.connection.close()


def get_transport(transport_name, host=None, port=None, login=None, password=None):
    available_transports = {'ssh': SSHTransport, 'sql': SQLTransport}
    transport_name = transport_name.lower()
    transport = available_transports.get(transport_name, None)
    if not transport:
        raise UnknownTransport('No such transport')
    host = get_system_host() if not host else host
    transport_data = get_transport_config(transport_name)
    port = transport_data['port'] if not port else port
    login = transport_data['login'] if not login else login
    password = transport_data['password'] if not password else password

    return transport(host, port, login, password)
