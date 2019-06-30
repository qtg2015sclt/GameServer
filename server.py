"""Game Server."""
# import sys
# sys.path.append('./network/')
# from simple_host import SimpleHost
import time
from network.simple_host import SimpleHost
from threadpool.threadpool import ThreadPool
from ecs.worldmgr import WorldMgr
from ecs.system.login_system import LoginSystem
from ecs.entity import entity


class GameServer(object):
    """GameServer."""

    def __init__(self):
        """A Game Server contains a simple host."""
        # self.worldmgr = WorldMgr()
        self.register_entity_and_system()
        self.worldmgr = WorldMgr()
        self.host = SimpleHost()
        return

    def start(self, port=0):
        """Start the server."""
        self.host.start_up(port)
        print 'GameServer start'
        while True:
            # network msg:
            self.host.process()
            # all other logic:
            self.worldmgr.update_all()
            time.sleep(0.01)
        return 0

    def register_entity_and_system(self):
        LoginSystem()
        entity.SingletonMgrEntity()


if "__main__" == __name__:
    port = 57890
    game_server = GameServer()
    try:
        game_server.start(port)
    except KeyboardInterrupt:
        print 'KeyboardInterrupt.'
        game_server.host.shut_down()
        pool = ThreadPool()
        pool.close()
