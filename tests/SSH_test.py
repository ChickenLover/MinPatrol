import pytest
from transports import *

def test_init():
        SSHTransport("localhost", 4500, "root", "pwd")
        with pytest.raises(TransportConnectionError):
            SSHTransport("localhost1", 4500, "root", "pwd")
            SSHTransport("localhost", 45001, "root", "pwd")
            SSHTransport("localhost", 4500, "root1", "pwd")
            SSHTransport("localhost", 4500, "root", "pwd1")

def test_exec():
    SSHTransport("localhost", 4500, "root", "pwd").exec("ls /")

def test_get_file():
    SSHTransport("localhost", 4500, "root", "pwd").get_file("/root/test")
    with pytest.raises(TransportIOError):
        SSHTransport("localhost", 4500, "root", "pwd").get_file("/root/test1")        

def test_get_transport():
    get_transport('ssh', "localhost", 4500, "root", "pwd")
    with pytest.raises(UnknownTransport):
        get_transport('ssh1', "localhost", 4500, "root", "pwd")
