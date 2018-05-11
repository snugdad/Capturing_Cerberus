from socket import *
from _thread import *
import sys
from time import *

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

try:
    listening_port = int(input("[*] Enter Listening Port Number: "))
except KeyboardInterrupt:
    print("\n [*] User terminated Application")
    sys.exit()
max_conn = 5
buff_size = 8192

def run():
    sock = AsyncSocket(socket(AF_INET, SOCK_STREAM))
    sock.bind(('', listening_port))
    print ("PASSED BIND")
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.listen(max_conn)
    print ("[*] Initializing Sockets ...")
    print ("Done\n")
    print ("[*] Binding...")
    print ("Done\n")
    print ("Server Started Successfully [ %d ]\n" % listening_port)
    while 1:
        try:
            conn, addr = sock.accept()
            data = conn.recv(buffer_size)
            start_new_thread(conn_string, (conn, data, addr))
        except KeyboardInterrupt:
            sock.close()
            print("User terminated Application")
            sys.exit(1)
    sock.close()

def conn_string(conn, data, addr):
    try:
        first_line = data.split('\n')[0]
        url = first_line.split(' ')[1]
        http_pos = url.find("://")
        if (http_pos == -1):
            temp = url
        else:
            temp = url[(http_pos + 3):]
        port_pos = temp.find(":")
        webserver_pos = temp.find("/")
        if webserver_pos == -1:
            webserver_pos = len(temp)
        webserver = ""
        port = -1
        if (port_pos == -1 or webserver_pos < port_pos):
            port = 80
            webserver = temp[:webserver_pos]
        else:
            port = int((temp[(port_pos + 1):])[:webserver_pos - pos_port - 1])
            webserver = temp[:port_pos]
        proxy_server(webserver, port, conn, addr, data)
    except Exception as e:
        pass

def proxy_server(webserver, port, conn, data, addr):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(webserver, port)
        s.send(data)
        while 1:
            reply = s.recv(buffer_size)
            if (len(reply) > 0):
                conn.send(reply)
                dar = float(len(reply))
                dar = float(dar / 1024)
                dar = "%.3s" % (str(dar))
                dar = "%s KB" % (dar)
                print ("[*] Request Finished: %s => %s <=" % (str(addr[0]), str(dar))) 
            else:
                break
        s.close()
        conn.close()
    except socket.error as e:
        s.close()
        conn.close()
        sys.exit(1)
run()
            