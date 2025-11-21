# -*- coding: utf-8 -*-
from jufufuBlockFrameAniScript.CodeCore.server.system.BaseServerSystem import BaseServerSystem
from jufufuBlockFrameAniScript.CodeCore.server.system.BaseServerSystem import BaseServerSystem
from jufufuBlockFrameAniScript.CodeCore.utils.eventWrapper import EngineEvent, AddonEvent
from jufufuBlockFrameAniScript.CodeCore.server import engineApiGas
from jufufuBlockFrameAniScript.CodeCore.common.api import commonApiMgr
from jufufuBlockFrameAniScript.modCommon import modConfig
from jufufuBlockFrameAniScript.CodeCore.server.api import serverApiMgr
import mod.server.extraServerApi as serverApi
compFactory = serverApi.GetEngineCompFactory()
minecraftEnum = serverApi.GetMinecraftEnum()

class SelectServerSystem(BaseServerSystem):

	def __init__(self, namespace, systemName):
		super(SelectServerSystem, self).__init__(namespace, systemName)
		self.Init()

	def Init(self):
		pass
	
	def Update(self):
		pass

	@AddonEvent(modConfig.ModNameSpace, modConfig.ClientSystemEnum.SelectClientSystem)
	def test123(self, args):
		print args


