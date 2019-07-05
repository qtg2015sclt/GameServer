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
        self.send_buffer = ''
        self.recv_buffer = ''
        self.closed = False

    # TODO: may need two type receive:
    # socket->buffer and buffer->host msg queue
    def receive(self):
        """Read socket and save to recv_buffer."""
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
        if '' == data:
            self.close()
        # return data
        self.recv_buffer += data

    def read_from_recv_buffer(self):
        """Read from recv_buffer."""
        data_list = self.recv_buffer.splitlines()
        self.recv_buffer = ''
        return data_list
        # raise NotImplementedError

    def send(self):
        """Send msg in send_buffer to socket."""
        if '' == self.send_buffer:
            # print 'BufferedSocket send: send_buffer is null, return.'
            return
        try:
            print 'BufferedSocket send: ', self.send_buffer
            self.sock.sendall(self.send_buffer)
            self.send_buffer = ''
        except socket.error, (code, strerror):
            print "Send msg failed, ", code, ": ", strerror
            self.close()

    def store_to_send_buffer(self, msg):
        """Store to send_buffer."""
        print 'BufferedSocket store_to_send_buffer: ' + msg
        self.send_buffer += (msg + '\n')
        # print self.send_buffer

    def close(self):
        """Close the socket."""
        # self.sock.shutdown(self.SHUTRDWR)
        print 'BufferedSocket close: ', self.sock.getpeername()
        # self.sock.close()
        # self.sock = None
        self.closed = True
