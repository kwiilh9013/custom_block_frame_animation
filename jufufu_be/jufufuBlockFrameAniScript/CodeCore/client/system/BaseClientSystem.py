# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
from jufufuBlockFrameAniScript.CodeCore.common.system.commonEventRegister import CommonEventRegister

ClientSystem = clientApi.GetClientSystemCls()


class BaseClientSystem(ClientSystem, CommonEventRegister):
	def __init__(self, namespace, systemName):
		ClientSystem.__init__(self, namespace, systemName)
		CommonEventRegister.__init__(self, self)
		
		self.mLevelId = clientApi.GetLevelId()
		self.mPlayerId = clientApi.GetLocalPlayerId()

	def Destroy(self):
		CommonEventRegister.OnDestroy(self)
