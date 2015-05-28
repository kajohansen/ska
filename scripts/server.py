#!/usr/bin/env python

import samba
from samba import param
from samba.samdb import SamDB
from samba.credentials import Credentials

import json

from autobahn.twisted.websocket import WebSocketServerProtocol, WebSocketServerFactory

class MySambaClass():
	
	def getUsers(self):
		lp = param.LoadParm()
		badge = Credentials()
		badge.guess(lp)
		badge.set_username('Administrator')
		badge.set_password('pa$$w0rd!')

		print("Getting users")
					
		# Binding...
		cx = SamDB(url='ldap://localhost', lp=lp, credentials=badge)

		# Search...
		search_result = cx.search('DC=kajohansen,DC=com', scope=2, expression='(objectClass=user)', attrs=["samaccountname"])
		
		users = [] # list to hold our users
		
		# Results...
		for username in search_result:
# 			print("User: %s" % username.get("samaccountname", idx=0))
			users.append(username.get("samaccountname", idx=0))
		
		return users


class MyServerProtocol(WebSocketServerProtocol):

	def onConnect(self, request):
		print("Client connecting: {0}".format(request.peer))

	def onOpen(self):
		print("WebSocket connection open.")

	def onMessage(self, payload, isBinary):
		
		if payload == "list-users":
			# echo back message verbatim
			# self.sendMessage(payload, isBinary)
			
			# print samba users
			samba = MySambaClass()
			users = samba.getUsers()
			
			self.sendMessage(json.dumps(users))
			
		else:
			print("Did not understand command")

	def onClose(self, wasClean, code, reason):
		print("WebSocket connection closed: {0}".format(reason))


if __name__ == '__main__':

	import sys
	
	from twisted.python import log
	from twisted.internet import reactor

	log.startLogging(sys.stdout)

	factory = WebSocketServerFactory("ws://localhost:9000", debug=False)
	factory.protocol = MyServerProtocol
	# factory.setProtocolOptions(maxConnections=2)

	reactor.listenTCP(9000, factory)
	reactor.run()

