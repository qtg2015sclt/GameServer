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
		self.sock.setsockopt(socket.SOL_SOCKET, socket.REUSEADDR, 1)
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

	def start(port = 0):
		self.create_server_socket()

		self.inputs = [self.sock]
		while True:
			readable, writable, exceptional = select.select(self.inputs, self.outputs, self.inputs)
			for s in readable:
				if s is self.sock:
					connection, client_address = s.accept()
					print 'connection from ' + client_address
					connection.setblocking(0)
					self.inputs.append(connection)
					self.message_queues[connection] = Queue.Queue()
				else:
					data = s.recv(1024)#.decode()
					if data:
						print 'received ' + data + ' from ' + s.getpeername()
						self.message_queues[s].put(data)
						if s not in self.outputs:
							outputs.append(s)
					else:
						print 'closing ' + client_address
						if s in self.outputs:
							self.outputs.remove(s)
						self.inputs.remove(s)
						s.close()
						del self.message_queues[s]
			for s in writable:
				try:
					next_msg = self.message_queues[s].get_nowait()
				except Queue.Empty:
					print s.getpeername() + ' queue empty'
					self.outputs.remove(s)
				else:
					print 'sending ' + next_msg + ' to ' + s.getpeername()
					s.send(next_msg)
			for s in exceptional:
				print 'exception condition on ' + s.getpeername()
				self.inputs.remove(s)
				if s in self.outputs:
					self.outputs.remove(s)
				s.close()
				del self.message_queues[s]

		return 0


if "__main__" == __name__:
	port = 23571
	game_server = GameServer()
	game_server.start(port)