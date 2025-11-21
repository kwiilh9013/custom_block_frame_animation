# -*- coding: utf-8 -*-
from jufufuBlockFrameAniScript.CodeCore.server.system.BaseServerSystem import BaseServerSystem


class ServerSystem(BaseServerSystem):

	def __init__(self, namespace, systemName):
		super(ServerSystem, self).__init__(namespace, systemName)
		self.Init()

	def Init(self):
		pass
	
	def Update(self):
		pass


