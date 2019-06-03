"""Network: SimpleHost."""
import sys
import json
import socket
import select
import conf
from buffered_socket import BufferedSocket
# sys.path.append('./dispatcher/')
# from dispatcher import Dispatcher
# from login_service import LoginService
# from game_service import GameSyncService
from dispatcher.dispatcher import Dispatcher
from dispatcher.login_service import LoginService
from dispatcher.game_service import GameSyncService


class SimpleHost(object):
    """A simple host."""

    def __init__(self):
        """Contain the socket, port and all connected sockets."""
        super(SimpleHost, self).__init__()

        self.sock = None
        self.port = 0
        self.SOCKETS = {}
        self.queue = []
        self.timeout = 0.01  # TODO: need set a more accurate number
        self.dispatcher = Dispatcher()
        service_dict = {
            LoginService.SID: LoginService(),
            # GameSyncService.SID: GameSyncService(),
        }
        self.dispatcher.registers(service_dict)

    def start_up(self, port=0):
        """Start the server socket."""
        self.shut_down()

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.sock.bind(('0.0.0.0', port))
        except Exception as e:
            try:
                print e
                self.sock.close()
            except Exception as e:
                print e
            return -1
        self.sock.listen(conf.MAX_HOST_CLIENTS_INDEX + 1)
        self.sock.setblocking(0)
        self.inputs = [self.sock]
        return

    def shut_down(self):
        """Shut down the server socket."""
        # TODO: need close client connection?
        if self.sock:
            self.sock.close()
        return

    def process(self):
        """Handle all situation.

        Handle new connection, read socket,
        Write socket, and remove closed socket.
        """
        read = [s.sock for s in self.SOCKETS.itervalues()]
        read += [self.sock]
        self.handle_new_connection(read)
        if 0 == len(self.SOCKETS):
            return
        read = write = [s.sock for s in self.SOCKETS.itervalues()]
        self.read_socket(read)
        self.write_socket(write)
        self.close()

    def handle_new_connection(self, read):
        """Handle new connection."""
        readable, _, _ = select.select(read, [], [], self.timeout)
        if self.sock in readable:
            connection, client_address = self.sock.accept()
            print >> sys.stderr, 'new connection from', client_address
            connection.setblocking(0)
            # when connection come, create a client(buffered socket):
            client = BufferedSocket(connection, client_address)
            self.SOCKETS.update({client.fileno: client})

    def read_socket(self, read):
        """Read the socket."""
        # for sock in self.SOCKETS.itervalues():
        #     print 'sock fileno = ', sock.fileno
        readable, _, exceptional = select.select(
            read,
            [],
            read,
            self.timeout
        )
        # print "readable count = ", readable.count()
        for s in readable:
            print s.fileno(), ' is readable'
            client = self.SOCKETS[s.fileno()]
            data = client.receive()
            if data:
                print 'received "%s" from %s' % (data, s.getpeername())
                # TODO: need handle dispatch return?
                self.dispatcher.dispatch(data, client)
        self.handle_exceptional(exceptional)

    def write_socket(self, write):
        """Send socket."""
        # TODO: outputs need get exceptional?
        # for msg in enumerate(self.queue):

        _, writable, exceptional = select.select(
            [],
            write,
            write,
            self.timeout
        )
        # TODO: cannot make a good broadcast
        for s in writable:
            # print s.fileno(), ' is writable'
            client = self.SOCKETS[s.fileno()]
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

    def close(self):
        """Remove all closed socket from map."""
        closed = [sock for sock in self.SOCKETS.itervalues() if sock.closed]
        for sock in closed:
            sock.sock.close()
            self.SOCKETS.pop(sock.fileno)

    def handle_exceptional(self, exceptional):
        """Handle exceptional."""
        for s in exceptional:
            print 'handling exceptional condition for', s.getpeername()
            self.SOCKETS.pop(s.fileno())
            s.close()
            # del self.message_send_queues[s]
