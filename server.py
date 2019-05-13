"""Game Server."""
from simple_host import SimpleHost
from dispatch import Dispatcher, LoginService, GameSyncService


class GameServer(object):
    """GameServer."""

    def __init__(self):
        """A Game Server contains a simple host."""
        self.host = SimpleHost()
        self.dispatcher = Dispatcher()
        service_dict = {
            LoginService.SERVICE_ID: LoginService,
            GameSyncService.SERVICE_ID: GameSyncService,
        }
        self.dispatcher.registers(service_dict)
        return

    def start(self, port=0):
        """Start the server."""
        self.host.start_up(port)
        while True:
            self.host.readSocket()
            self.host.sendSocket()
        return 0


if "__main__" == __name__:
    port = 57890
    game_server = GameServer()
    try:
        game_server.start(port)
    except KeyboardInterrupt:
        game_server.shutDown()
