"""Network: BufferedSocket."""
import socket


class BufferedSocket(object):
    """Package the socket connetion with buffer."""

    def __init__(self, sock, addr):
        """A buffered socket contains socket and buffer."""
        super(BufferedSocket, self).__init__
        self.sock = sock
        self.fileno = sock.fileno()
        self.addr = addr
        self.sock.setblocking(0)
        # self.send_buffer = ''
        # self.recv_buffer = ''
        self.closed = False

    def receive(self):
        """Read socket."""
        # data = ''
        data = self.sock.recv(4096)
        # while True:
        #     chunk = ''
        #     try:
        #         chunk = self.sock.recv(4096)
        #         if not chunk:
        #             print 'read no data, closing ', self.sock.getpeername()
        #             self.close()
        #     except socket.error, (code, strerror):
        #         print "Receive data failed, ", code, ": ", strerror
        #         self.close()
        #     if '' == chunk:
        #         break
        #     data += chunk
        return data

    def send(self, msg):
        """Send msg to socket."""
        try:
            self.sock.sendall(msg)
        except socket.error, (code, strerror):
            print "Send msg failed, ", code, ": ", strerror
            self.close()

    def close(self):
        """Close the socket."""
        # self.sock.shutdown(self.SHUTRDWR)
        self.sock.close()
        self.sock = None
        self.closed = True
