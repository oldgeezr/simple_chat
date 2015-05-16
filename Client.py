# -*- coding: utf-8 -*-
from MessageReceiver import MessageReceiver
import json
import socket
import re
import time

class Client:
	"""
	This is the chat client class
	"""

	def __init__(self, host, server_port):
		"""
		This method is run when creating a new Client object
		"""
		# Set up the socket connection to the server
		self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connection.connect((host, server_port))
		self.run()

		print "Welcome to login menu\n Login: login <username>"
		while True:
			data = raw_input('\n>> ')
			self.send_payload(data)
			time.sleep(0.1)

	def run(self):
		# Initiate the connection to the server
		server_thread = MessageReceiver(self, self.connection)
		server_thread.daemon = True
		server_thread.start()

	def disconnect(self):
		# TODO: Handle disconnection
		self.connection.force_disconnect()

	def receive_message(self, message):
		data = json.loads(message)

		if data.get('response') == 'error':
			# print error message
			print data.get('content')
		elif data.get('response') == 'info':
			if data.get('content') == 'logout':
				print 'Goodbye ' + data.get('sender') + '!'
			else:
				print "Online users:" + data.get('content')
		elif data.get('response') == 'history':
			history = data.get('content') # list of JSON responses
			print 'Welcome ' + data.get('sender') + '! ' + history
		elif data.get('response') == 'message':
			# print message
			print self.print_formatted(data.get('sender'),data.get('timestamp'),data.get('content'))

	def send_payload(self, data):
		# WIP
		if re.match('login\s+(\S+)\s*$', data):
			username = re.match('login\s+(\S+)\s*$', data).group(1)
			#username = data.lstrip('login ')
			data = self.msg_format('login', username)
			self.connection.sendall(json.dumps(data))
		elif data.startswith('logout'):
			data = self.msg_format('logout', None)
			self.connection.sendall(json.dumps(data))
    #elif re.match('msg\s+(.*)$', data):
      # TODO: remove the msg command
      #message = re.match('msg\s+(.*)$', data).group(1)
      #print message
      #data = self.msg_format('msg', message)
      #self.connection.sendall(json.dumps(data))
		elif data.startswith('help'):
			data = self.msg_format('help', None)
			self.connection.sendall(json.dumps(data))
		elif data.startswith('names'):
			data = self.msg_format('names', None)
			self.connection.sendall(json.dumps(data))
		else:
			if len(data) > 0:
        # send msg
				data = self.msg_format('msg', data)
				self.connection.sendall(json.dumps(data))
			else:
				print 'Not a valid command!'

	def msg_format(self, request, content):
		# Wait for data from the client
		return {'request': request, 'content': content}

	def print_formatted(self, sender, timestamp, message):
		return sender + ' said @ ' + timestamp + ': ' + message

if __name__ == '__main__':
	"""
	This is the main method and is executed when you type "python Client.py"
	in your terminal.

	No alterations is necessary
	"""

	client = Client('78.91.6.89', 9998)
