class Dispatcher(object):
	def __init__(self):
		super(Dispatcher, self).__init__()
		self.services = {}

	def dispatch(self, msg, owner):
		svcid = msg.svcid
		if not svcid in self.services:
			raise Exception('bad service %d' % svcid)
		svc = self.services[svcid]
		return svc.handle(msg, owner)

	def registers(self, service_dict):
		self.services = {}
		for svcid in service_dict:
			self.services[svcid] = service_dict[svcid]

class Service(object):
	def __init__(self, svcid):
		super(Service, self).__init__()
		self.service_id = svcid
		self.commands = {}

	def handle(self, msg, owner):
		cmdid = msg.cmdid
		if not cmdid in self.commands:
			raise Exception('bad command %s' % cmdid)

		f = self.commands[cmdid]
		return f(msg, owner)
		#raise NotImplementedError

	def registers(self, command_dict):
		self.commands = {}
		for cmdid in command_dict:
			self.commands[cmdid] = command_dict[cmdid]

class LoginService(Service):
	SERVICE_ID = 1000
	HandleLoginCmdID = 1001

	def __init__(self):
		super(LoginService, self).__init__(self.SERVICE_ID)
		command_dict = {
		self.HandleLoginCmdID: self.handleLogin,
		}
		self.registers(command_dict)

	def handleLogin(self, msg, who):
		raise NotImplementedError

class GameSyncService(Service):
	SERVICE_ID = 2000
	ClientSyncCmdID = 1001

	def __init__(self):
		super(GameSyncService, self.__init__(self.SERVICE_ID))
		command_dict = {
		self.ClientSyncCmdID: self.playerSync,
		}
		self.registers(command_dict)

	def playerSync(self, msg, who):
		raise NotImplementedError
