"""Network."""


class BufferedSocket(object):
    """Package the socket connetion with buffer."""

    def __init__(self, sock):
        """A buffered socket contains socket and buffer."""
        super(BufferedSocket, self).__init__
        self.sock = None
        self.sock.setblocking(0)
        self.buffer
        self.closed = False

    def receive(self):
        """Read socket."""
        chunk = self.sock.recv(4096)
        if b'' == chunk:
            self.closed = True
        self.buffer += chunk

    def send(self, msg):
        """Send msg to socket."""
        sent = self.sock.send(msg)
        return sent

    def close(self):
        """Close the socket."""
        self.sock.shutdown(self.SHUTRDWR)
        self.sock.close()
        self.sock = None
        self.closed = True
