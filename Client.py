# -*- coding: utf-8 -*-
from MessageReceiver import MessageReceiver
import json
import socket

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
        self.run()

        # TODO: Finish init process with necessary code
        server_thread = MessageReceiver(client, self.connection)
        server_thread.start() 
        
        while True:
            data = raw_input('>> ')
            self.send_payload(data)
        
    def run(self):
        # Initiate the connection to the server
        self.connection.connect((self.host, self.server_port))

    def disconnect(self):
        # TODO: Handle disconnection
        self.connection.close()

    def receive_message(self, message):
        # TODO: Handle incoming message
        data = json.loads(message)

        if data.get('response') == 'error':
            # print error message
            print data.get('content')
            
        elif data.get('response') == 'info':
            if data.get('content') == 'logout':
                print 'Goodbye ' + data.get('sender') + '!'
                self.disconnect()
            else:
                print data.get('content')

        elif data.get('response') == 'history':
            print 'Welcome ' + data.get('sender') + '!'
            history = data.get('content') # list of JSON responses
            # print history
            
        elif data.get('response') == 'message':
            # print message
            print print_formatted(data.get('sender'),data.get('timestamp'),data.get('content'))
        

    def send_payload(self, data):
        # WIP
        if data.startswith("login"):
            username = data.lstrip('login ')
            data = msg_format('login', username)
            self.connection.sendall(json.dumps(data))
            
        elif data.startswith("logout"):
            data = msg_format('logout', None)
            self.connection.sendall(json.dumps(data))
            
        elif data.startswith("msg"):
            message = data.lstrip('msg ')
            data = msg_format('msg', message)
            self.connection.sendall(json.dumps(data))
            
        elif data.startswith("help"):
            data = msg_format('help', None)
            self.connection.sendall(json.dumps(data))
            
        elif data.startswith("names"):
            data = msg_format('names', None)
            self.connection.sendall(json.dumps(data))
            
        else:
            print data.split()[0] + ' is not a valid command!'
        


    def msg_format(request, content):                                                 
        # Wait for data from the client
        return {'request': request, 'content': content}

    def print_formatted(sender,timestamp,message):
        return sender + ' said @ ' + timestamp + ': ' + message


if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations is necessary
    """
    
    client = Client('localhost', 9998)
