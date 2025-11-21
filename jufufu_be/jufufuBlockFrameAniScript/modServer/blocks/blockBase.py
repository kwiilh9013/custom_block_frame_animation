# -*- coding: UTF-8 -*-
import mod.server.extraServerApi as serverApi
from jufufuBlockFrameAniScript.CodeCore.utils.eventWrapper import EngineEvent
from jufufuBlockFrameAniScript.CodeCore.common.system.commonEventRegister import CommonEventRegister
from jufufuBlockFrameAniScript.modCommon.cfg.blocks import blocksConfig
compFactory = serverApi.GetEngineCompFactory()
minecraftEnum = serverApi.GetMinecraftEnum()


class BlockBase(CommonEventRegister):
	"""方块逻辑 基类"""
	def __init__(self, severHandler, playerId, blockName, pos, dimension, param={}):
		CommonEventRegister.__init__(self, severHandler)
		self.mServer = severHandler
		self.mLevelId = self.mServer.mLevelId
		self.mPlayerId = playerId
		self.mBlockName = blockName
		self.mPos = pos
		self.mDimension = dimension
		
		self.mBlockEntityComp = compFactory.CreateBlockEntityData(self.mLevelId)

		# 获取config，设置参数
		self.mCfg = blocksConfig.GetFunctionalBlockConfig(blockName)

		# 初始化一遍玩家id
		self.GetPlayerId()
		pass

	def Destroy(self):
		CommonEventRegister.OnDestroy(self)
		if self.mServer:
			self.mServer.ClearBlockObjDict(self.mPos, self.mDimension)
		self.mServer = None
		# 清除对象自己
		del self
		pass
	
	# region 事件
	@EngineEvent()
	def BlockRemoveServerEvent(self, args):
		"""方块销毁事件"""
		blockName = args.get("fullName")
		dimension = args.get("dimension")
		pos = (args.get("x"), args.get("y"), args.get("z"))
		if blockName == self.mBlockName and dimension == self.mDimension and pos == self.mPos:
			self.Destroy()
		pass
	# endregion

	def IsCheck(self, entityId):
		"""判断是否可触发"""
		# 24.12修改：所有玩家、被玩家驯服的生物、车，不会触发
		if entityId in serverApi.GetPlayerList():
			return False
		tameComp = compFactory.CreateTame(entityId)
		oid = tameComp.GetOwnerId()
		if oid:
			return False
		attrComp = serverApi.GetEngineCompFactory().CreateAttr(entityId)
		family = attrComp.GetTypeFamily()
		if "car" in family or "npc" in family or "inanimate" in family:
			return False
		return True

	def GetPlayerId(self):
		"""获取玩家id"""
		# 如果传递的玩家id为空，则读取方块数据，获取到玩家id
		if not self.mPlayerId:
			blockData = self.mBlockEntityComp.GetBlockEntityData(self.mDimension, self.mPos)
			if blockData:
				data = blockData[blocksConfig.BlockEntityDataKey]
				if data:
					self.mPlayerId = data.get("playerId")
		else:
			# 保存一次玩家id
			self.SavePlayerId()
		return self.mPlayerId

	def SavePlayerId(self):
		"""保存玩家id"""
		if self.mPlayerId:
			blockData = self.mBlockEntityComp.GetBlockEntityData(self.mDimension, self.mPos)
			if blockData:
				data = blockData[blocksConfig.BlockEntityDataKey]
				if data is None:
					data = {}
				data["playerId"] = self.mPlayerId
				blockData[blocksConfig.BlockEntityDataKey] = data
		pass
