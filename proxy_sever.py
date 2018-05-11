from socket import *
from concurrent.futures import ProcessPoolExecutor as ProcessPoolExecutor
from collections import deque
from select import select
tasks = deque()
recv_wait = { }
send_wait = { }
future_wait = { }

future_notify, future_event = socketpair()
class AsyncSocket(object):
    def __init__(self, sock):
        self.sock = sock
    def recv(self, maxsize):
        yield 'recv', self.sock
        return self.sock.recv(maxsize)
    def send(self, data):
        yield 'send', self.sock
        return self.sock.send(data)
    def accept(self):
        yield 'recv', self.sock
        client, addr = self.sock.accept()
        return AsyncSocket(client), addr
    def __getattr__(self, name):
        return getattr(self.sock, name)

def proxy_server(address):
    sock = AsyncSocket(socket(AF_INET, SOCK_STREAM))
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(5);
    while True:
        client, addr = yield from sock.accept()
        print("Connection Established: ", addr)
        