# -*- coding: utf-8 -*-
from jufufuBlockFrameAniScript.CodeCore.client.system.BaseClientSystem import BaseClientSystem
from jufufuBlockFrameAniScript.CodeCore.utils.eventWrapper import EngineEvent, AddonEvent
from jufufuBlockFrameAniScript.modCommon import modConfig
import mod.client.extraClientApi as clientApi
from jufufuBlockFrameAniScript.modClient.manager.singletonGac import Instance
from jufufuBlockFrameAniScript.modClient.manager.clientMgrList import ClientManagerList
import re

compFactory = clientApi.GetEngineCompFactory()
minecraftEnum = clientApi.GetMinecraftEnum()
EntityTypeEnum = clientApi.GetMinecraftEnum().EntityType


class ClientSystem(BaseClientSystem):
	def __init__(self, namespace, systemName):
		super(ClientSystem, self).__init__(namespace, systemName)
		self._loadCompleted = False
		self.InitManager()

	@EngineEvent()
	def LoadClientAddonScriptsAfter(self, args=None):
		pass

	def InitManager(self):
		print("==========InitManager=========")
		strinfo = re.compile(r'Gac$')
		for mgrCls in ClientManagerList:
			mgr = mgrCls(self)
			setattr(Instance, "m" + strinfo.sub("", mgrCls.__name__), mgr)

	@EngineEvent(priority=10)
	def UiInitFinished(self, args):
		# 这里需要把优先级提到最高，否则其他模块在该事件时设置UI，可能会设置失败
		Instance.mUIManager.UiInitFinished(args)