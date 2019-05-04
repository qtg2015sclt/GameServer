import socket
import select
import sys
import Queue
import conf

class GameServer(object):
	def __init__(self):
		self.sock = None
		self.inputs = []
		self.outputs = []
		self.message_queues = {}
		return

	def create_server_socket(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		try:
			self.sock.bind(('0.0.0.0', port))
		except:
			try:
				self.sock.close()
			except:
				pass #should logging here
			return -1
		self.sock.listen(conf.MAX_HOST_CLIENTS_INDEX+1)
		self.sock.setblocking(0)
		return

	def shut_down(self):
		self.sock.close()
		return

	def start(self, port = 0):
		self.create_server_socket()

		self.inputs = [self.sock]
		while True:
			readable, writable, exceptional = select.select(self.inputs, self.outputs, self.inputs)
			for s in readable:
				if s is self.sock:
					connection, client_address = s.accept()
					print >> sys.stderr, 'new connection from', client_address
					connection.setblocking(0)
					self.inputs.append(connection)
					self.message_queues[connection] = Queue.Queue()
				else:
					data = s.recv(1024)#.decode()
					if data:
						print >> sys.stderr, 'received "%s" from %s' % (data, s.getpeername())
						self.message_queues[s].put(data + '\n')
						if s not in self.outputs:
							self.outputs.append(s)
					else:
						print >> sys.stderr, 'closing', client_address, 'after reading no data'
						if s in self.outputs:
							self.outputs.remove(s)
						self.inputs.remove(s)
						s.close()
						del self.message_queues[s]
			for s in writable:
				try:
					next_msg = self.message_queues[s].get_nowait()
				except Queue.Empty:
					print >> sys.stderr, 'output queue for', s.getpeername(), 'is empty'
					self.outputs.remove(s)
				else:
					print >> sys.stderr, 'sending "%s" to %s' % (next_msg, s.getpeername())
					s.send(next_msg)
			for s in exceptional:
				print >> sys.stderr, 'handling exceptional condition for', s.getpeername()
				self.inputs.remove(s)
				if s in self.outputs:
					self.outputs.remove(s)
				s.close()
				del self.message_queues[s]

		return 0


if "__main__" == __name__:
	port = 57890
	game_server = GameServer()
	try:
		game_server.start(port)
	except KeyboardInterrupt:
		game_server.shut_down()