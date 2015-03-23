# -*- coding: utf-8 -*-
import SocketServer
import json
import time
import datetime
import re

class ClientHandler(SocketServer.BaseRequestHandler):
	"""
	This is the ClientHandler class. Everytime a new client connects to the
	server, a new ClientHandler object will be created. This class represents
	only connected clients, and not the server itself. If you want to write
	logic for the server, you must write it outside this class
	"""
	history = []
	clients = {}

	def login(self, json_object):
		username = json_object.get('content')
		pattern = '^\w+$'

		if not re.match(pattern, username):
			return_data = self.msg_format(username, 'error', 'Invalid username!')
			self.connection.sendall(json.dumps(return_data))
		elif username in self.clients.values():
			return_data = self.msg_format(username, 'error', 'Name already taken!')
			self.connection.sendall(json.dumps(return_data))
		else:
			self.clients[self.connection] = username
			messages = ""
			for message in self.history:
				messages += '\n' + message
			return_data = self.msg_format(username, 'history', messages)
			self.connection.sendall(json.dumps(return_data))


	def logout(self):
		if not self.connection in self.clients:
			return_data = self.msg_format(None, 'error', 'Not logged in!')
			self.connection.sendall(json.dumps(return_data))
		else:
			username = self.clients[self.connection]
			return_data = self.msg_format(username, 'info', 'logout')
			self.connection.sendall(json.dumps(return_data))
			del self.clients[self.connection]
			print self.clients

	def send_payload(self, json_object):
		if not self.connection in self.clients:
			return_data = self.msg_format(None, 'error', 'Not logged in!')
			self.connection.sendall(json.dumps(return_data))
		else:
			username = self.clients[self.connection]
			json_message = json_object.get('content')
			return_data = self.msg_format(username, 'message', json_message)
			message = self.print_formatted(username, json_message)
			self.history.append(message)
			self.broadcast(json.dumps(return_data))

	def send_info(self, info):
		if not self.connection in self.clients:
			return_data = self.msg_format(None, 'error', 'Not logged in!')
			self.connection.sendall(json.dumps(return_data))
		else:
			if info == 'names':
				names = ""
				for username in self.clients.values():
					names += '\n' + username
				return_data = self.msg_format(None, 'info', names)
				self.connection.sendall(json.dumps(return_data))
			else:
				return_data = self.msg_format(None, 'info', 'You are on your own')
				self.connection.sendall(json.dumps(return_data))

	def print_formatted(self, sender, message):
		ts = time.time()
		timestamp = datetime.datetime.fromtimestamp(ts).strftime('%d.%m.%Y %H:%M:%S')

		return sender + ' said @ ' + timestamp + ': ' + message

	def msg_format(self, sender, response, content):
		ts = time.time()
		timestamp = datetime.datetime.fromtimestamp(ts).strftime('%d.%m.%Y %H:%M:%S')

		return {'timestamp'	: timestamp,
				'sender'	: sender,
				'response'	: response,
				'content'	: content}

	def broadcast(self, message):
		for client in self.clients:
			client.sendall(message)

	def handle(self):
		"""
		This method handles the connection between a client and the server.
		"""
		self.ip = self.client_address[0]
		self.port = self.client_address[1]
		self.connection = self.request

		print 'Client connected @' + self.ip + ':' + str(self.port)

		# Loop that listens for messages from the client
		while True:
			received_string = self.connection.recv(4096)
			if received_string:
				json_object = json.loads(received_string)
				request = json_object.get('request')

				if request == 'login':
					self.login(json_object)
				elif request == 'logout':
					self.logout()
				elif request == 'names' or request == 'help':
					self.send_info(request)
				elif request == 'msg':
					self.send_payload(json_object)
			else:
				break

		print 'Client disconnected @' + self.ip + ':' + str(self.port)

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
	"""
	This class is present so that each client connected will be ran as a own
	thread. In that way, all clients will be served by the server.

	No alterations is necessary
	"""
	allow_reuse_address = True

if __name__ == "__main__":
	"""
	This is the main method and is executed when you type "python Server.py"
	in your terminal.

	No alterations is necessary
	"""
	HOST, PORT = 'localhost', 9998
	print 'Server running...'

	# Set up and initiate the TCP server
	server = ThreadedTCPServer((HOST, PORT), ClientHandler)
	server.serve_forever()
