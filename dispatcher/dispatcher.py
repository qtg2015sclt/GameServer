"""Dispatch network msg to services."""
import json


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
        # print 'Dispatcher dispatch:', svc
        svc.handle(msg, owner)

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
        f(msg, owner)

    def registers(self, command_dict):
        """Register commands."""
        self.commands = {}
        for cid in command_dict:
            self.commands[cid] = command_dict[cid]
