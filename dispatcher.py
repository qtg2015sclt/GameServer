"""Dispatch network msg to services."""
import json
import pymongo


class Dispatcher(object):
    """Dispatch network msg."""

    def __init__(self):
        """Contain registered services."""
        super(Dispatcher, self).__init__()
        self.services = {}

    def dispatch(self, data, owner):
        """Dispatch msg to Service class."""
        msg = json.loads(data)
        sid = msg["SID"]
        if sid not in self.services:
            raise Exception('bad service %d' % sid)
        svc = self.services[sid]
        print svc
        return svc.handle(msg, owner)

    def registers(self, service_dict):
        """Register services."""
        self.services = {}
        for sid in service_dict:
            self.services[sid] = service_dict[sid]


class Service(object):
    """Father of all certain services."""

    def __init__(self, sid):
        """Contain self service id and all commands dict."""
        super(Service, self).__init__()
        self.service_id = sid
        self.commands = {}

    def handle(self, msg, owner):
        """Dispatch msg to a certain services."""
        cid = msg["CID"]
        if cid not in self.commands:
            raise Exception('bad command %s' % cid)

        f = self.commands[cid]
        return f(msg, owner)

    def registers(self, command_dict):
        """Register commands."""
        self.commands = {}
        for cid in command_dict:
            self.commands[cid] = command_dict[cid]


class LoginService(Service):
    """Handle login."""

    SERVICE_ID = 1000
    HandleLoginCmdID = 1001

    def __init__(self):
        """Register all handle functions."""
        super(LoginService, self).__init__(self.SERVICE_ID)
        command_dict = {
            self.HandleLoginCmdID: self.handle_login,
        }
        self.registers(command_dict)

    def handle_login(self, msg, who):
        """Handle login."""
        username = msg["UserName"]
        password = msg["Password"]
        # print 'Login data: username = ', username, ", password = ", password
        # db host and port for test
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["tpsdemo"]
        col = db["LocalAuth"]
        myquery = {"username": username, "password": password}
        try:
            res = col.find(myquery).limit(1)[0]
        except:
            print "No such user"
            raise Exception("No such user")
        userid = res["userid"]
        print "userid = ", userid


class GameSyncService(Service):
    """Game sync service."""

    SERVICE_ID = 2000
    ClientSyncCmdID = 1001

    def __init__(self):
        """Register all handle functions."""
        super(GameSyncService, self).__init__(self.SERVICE_ID)
        command_dict = {
            self.ClientSyncCmdID: self.player_sync,
        }
        self.registers(command_dict)

    def player_sync(self, msg, who):
        """Sync msg of players."""
        raise NotImplementedError
