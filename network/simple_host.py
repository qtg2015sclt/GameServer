"""Network: SimpleHost."""
import sys
import socket
import select
import conf
from buffered_socket import BufferedSocket


class SimpleHost(object):
    """A simple host."""

    def __init__(self):
        """A simple host contains the socket, port and socket2client map."""
        super(SimpleHost, self).__init__()

        self.sock = None
        self.port = 0
        self.socket_client_map = {}

    def start_up(self, port=0):
        """Start the server socket."""
        self.shut_down()

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.sock.bind(('0.0.0.0', port))
        except:
            try:
                self.sock.close()
            except:
                pass  # should logging here
            return -1
        self.sock.listen(conf.MAX_HOST_CLIENTS_INDEX + 1)
        self.sock.setblocking(0)
        self.inputs = [self.sock]
        return

    def shut_down(self):
        """Shut down the server socket."""
        # TODO: need close client connection?
        self.sock.close()
        return

    def read_socket(self):
        """Read the socket."""
        readable, _, exceptional = select.select(self.inputs, [], self.inputs)
        for s in readable:
            if s is self.sock:
                connection, client_address = s.accept()
                print >> sys.stderr, 'new connection from', client_address
                connection.setblocking(0)
                # when connection come, create a client(buffered socket):
                client = BufferedSocket(connection)
                self.socket_client_map[connection] = client
            else:
                data = s.recv(1024)  # .decode()
                if data:
                    print 'received "%s" from %s' % (data, s.getpeername())
                    # self.message_send_queues[s].put(data + '\n')
                    if s not in self.outputs:
                        self.outputs.append(s)
                        # TODO: need handle dispatch return?
                        self.dispatcher.dispatch(data)
                    else:
                        print 'read no data, closing ', client_address
                        if s in self.outputs:
                            self.outputs.remove(s)
                        self.inputs.remove(s)
                        s.close()
                        del self.message_send_queues[s]
            for s in exceptional:
                print 'handling exceptional condition for', s.getpeername()
                self.inputs.remove(s)
                if s in self.outputs:
                    self.outputs.remove(s)
                s.close()
                del self.message_send_queues[s]

    def send_socket(self):
        """Send socket."""
        # TODO: outputs need get exceptional?
        _, writable, exceptional = select.select([], self.outputs, self.outputs)
        # TODO: cannot make a good broadcast
        for s in writable:
            try:
                next_msg = self.message_send_queues[s].get_nowait()
            except Queue.Empty:
                print 'output queue for', s.getpeername(), 'is empty'
                self.outputs.remove(s)
            else:
                print 'sending "%s" to %s' % (next_msg, s.getpeername())
                s.send(next_msg)
            for s in exceptional:
                print 'handling exceptional condition for', s.getpeername()
                self.inputs.remove(s)
                if s in self.outputs:
                    self.outputs.remove(s)
                s.close()
                del self.message_send_queues[s]
