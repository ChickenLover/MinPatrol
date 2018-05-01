from min_patrol import *

def main():
    try:
        get_transport("SSH", "localhost", 4500, "root", "pwd").get_file("/root/test")
    except TransportIOError:
        return 2
    except TransportConnectionError:
        return 4
    return 1
