"""Network: SimpleHost."""
import sys
import socket
import select
import conf
from buffered_socket import BufferedSocket
from dispatch import Dispatcher, LoginService, GameSyncService


class SimpleHost(object):
    """A simple host."""

    def __init__(self):
        """A simple host contains the socket, port and socket2client map."""
        super(SimpleHost, self).__init__()

        self.sock = None
        self.port = 0
        self.socket_client_map = {}
        self.dispatcher = Dispatcher()
        service_dict = {
            LoginService.SERVICE_ID: LoginService,
            GameSyncService.SERVICE_ID: GameSyncService,
        }
        self.dispatcher.registers(service_dict)

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

    def process(self):
        """Handle new connection, read socket, write socket."""
        read = [s.sock for s in self.socket_client_map.itervalues()]
        read += [self.sock]
        self.handle_new_connection(read)
        read = write = [s.sock for s in self.socket_client_map.itervalues()]
        self.read_socket(read)
        self.write_socket(write)

    def handle_new_connection(self, read):
        """Handle new connection."""
        readable, _, _ = select.select(read, [], [])
        if self.sock in readable:
            connection, client_address = self.sock.accept()
            print >> sys.stderr, 'new connection from', client_address
            connection.setblocking(0)
            # when connection come, create a client(buffered socket):
            client = BufferedSocket(connection)
            self.socket_client_map.update({connection: client})

    def read_socket(self, read):
        """Read the socket."""
        readable, _, exceptional = select.select(read, [], read)
        for s in readable:
            client = self.socket_client_map[s]
            data = client.receive()
            if data:
                print 'received "%s" from %s' % (data, s.getpeername())
                # self.message_send_queues[s].put(data + '\n')
                # TODO: need handle dispatch return?
                self.dispatcher.dispatch(data)
            else:
                print 'read no data, closing ', s.getpeername()
                if s in self.socket_client_map.iterkeys():
                    self.socket_client_map.remove(s)
                    s.close()
                    # del self.message_send_queues[s]
        self.handle_exceptional(exceptional)

    def write_socket(self, write):
        """Send socket."""
        # TODO: outputs need get exceptional?
        _, writable, exceptional = select.select([], write, write)
        # TODO: cannot make a good broadcast
        for s in writable:
            client = self.socket_client_map[s]
            client.send()
            # try:
            #     next_msg = self.message_send_queues[s].get_nowait()
            # except Queue.Empty:
            #     print 'output queue for', s.getpeername(), 'is empty'
            #     self.outputs.remove(s)
            # else:
            #     print 'sending "%s" to %s' % (next_msg, s.getpeername())
            #     s.send(next_msg)
        self.handle_exceptional(exceptional)

    def handle_exceptional(self, exceptional):
        """Handle exceptional."""
        for s in exceptional:
            print 'handling exceptional condition for', s.getpeername()
            self.socket_client_map.remove(s)
            s.close()
            # del self.message_send_queues[s]
