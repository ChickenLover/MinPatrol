import pytest
from transports import *

def test_init():
        SQLTransport("localhost", 4500, "root", "pwd")
        with pytest.raises(TransportConnectionError):
            SQLTransport("localhost1", 4500, "root", "pwd")
            SQLTransport("localhost", 45001, "root", "pwd")
            SQLTransport("localhost", 4500, "root1", "pwd")
            SQLTransport("localhost", 4500, "root", "pwd1")

def test_exec():
    SQLTransport("localhost", 4500, "root", "pwd").exec("ls /")

def test_get_transport():
    get_transport('sql', "localhost", 4500, "root", "pwd")
    with pytest.raises(UnknownTransport):
        get_transport('sql1', "localhost", 4500, "root", "pwd")
