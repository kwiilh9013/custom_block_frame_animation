# -*- coding: utf-8 -*-
import mod.server.extraServerApi as serverApi
import mod.client.extraClientApi as clientApi
from mod.common.mod import Mod
from jufufuBlockFrameAniScript.modCommon import modConfig


@Mod.Binding(name=modConfig.ModName, version=modConfig.ModVersion)
class ModMain(object):

	@Mod.InitServer()
	def ServerInit(self):
		ServerSystemList = modConfig.ServerSystemList
		for systemName in ServerSystemList:
			serverApi.RegisterSystem(
				modConfig.ModNameSpace,
				systemName,
				"%s.%s.%s" % (modConfig.ServerSystemPath, systemName, systemName))

	@Mod.DestroyServer()
	def ServerDestroy(self):
		pass

	@Mod.InitClient()
	def ClientInit(self):
		for systemName in modConfig.ClientSystemList:
			clientApi.RegisterSystem(
				modConfig.ModNameSpace,
				systemName,
				"%s.%s.%s" % (modConfig.ClientSystemPath, systemName, systemName))

	@Mod.DestroyClient()
	def ClientDestroy(self):
		pass
