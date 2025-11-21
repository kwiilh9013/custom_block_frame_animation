# -*- coding: UTF-8 -*-
import mod.server.extraServerApi as serverApi
from jufufuBlockFrameAniScript.CodeCore.utils.eventWrapper import EngineEvent
from jufufuBlockFrameAniScript.CodeCore.common.system.commonEventRegister import CommonEventRegister
from jufufuBlockFrameAniScript.modCommon.cfg.entity import entityConfig
compFactory = serverApi.GetEngineCompFactory()
minecraftEnum = serverApi.GetMinecraftEnum()


class EntityBase(CommonEventRegister):
	def __init__(self, severHandler, entityId, engineTypeStr=None, param={}):
		CommonEventRegister.__init__(self, severHandler)
		self.mServer = severHandler
		self.mLevelId = self.mServer.mLevelId
		self.mEntityId = entityId
		self.mEngineTypeStr = engineTypeStr
		
		self.mCfg = entityConfig.GetEntityConfig(engineTypeStr)
		
		pass

	def Destroy(self):
		CommonEventRegister.OnDestroy(self)
		self.mServer = None
		del self
		pass

	@EngineEvent()
	def EntityRemoveEvent(self, args):
		entityId = args.get("id")
		if entityId == self.mEntityId:
			self.Destroy()
		pass
