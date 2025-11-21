import mod.server.extraServerApi as serverApi
from jufufuBlockFrameAniScript.CodeCore.common.log.logMetaClass import LogMetaClass
from jufufuBlockFrameAniScript.CodeCore.common.system.commonEventRegister import CommonEventRegister
from jufufuBlockFrameAniScript.CodeCore.server import engineApiGas
ServerSystem = serverApi.GetServerSystemCls()


class BaseServerSystem(ServerSystem, CommonEventRegister):
	__metaclass__ = LogMetaClass

	def __init__(self, namespace, systemName):
		ServerSystem.__init__(self, namespace, systemName)
		CommonEventRegister.__init__(self, self)

		self.mLevelId = serverApi.GetLevelId()
		pass

	def Destroy(self):
		CommonEventRegister.OnDestroy(self)
