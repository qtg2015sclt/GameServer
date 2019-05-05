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
		raise NotImplementedError

	def registers(self, command_dict):
		self.commands = {}
		for cmdid in command_dict:
			self.commands[cmdid] = command_dict[cmdid]
