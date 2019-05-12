"""Game Server."""
import socket
import select
import sys
import Queue
import conf
from dispatch import Dispatcher, LoginService, GameSyncService


class GameServer(object):
    """GameServer."""

    def __init__(self):
        """Init."""
        self.sock = None
        self.inputs = []
        self.outputs = []
        self.socket_player_map = {}
        self.message_send_queues = {}
        self.dispatcher = Dispatcher()
        service_dict = {
            LoginService.SERVICE_ID: LoginService,
            GameSyncService.SERVICE_ID: GameSyncService,
        }
        self.dispatcher.registers(service_dict)
        return

    def create_server_socket(self, port=0):
        """Create a server socket."""
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
        """Shut down the server."""
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
                # when connection come, add to inputs list:
                self.inputs.append(connection)
                #  then create a msg send Q for it:
                self.message_send_queues[connection] = Queue.Queue()
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

    def start(self):
        """Start the server."""
        while True:
            self.readSocket()
            self.sendSocket()
        return 0


if "__main__" == __name__:
    port = 57890
    game_server = GameServer()
    try:
        game_server.createServerSocket(port)
        game_server.start()
    except KeyboardInterrupt:
        game_server.shutDown()
