# -*- coding: utf-8 -*-
from jufufuBlockFrameAniScript.CodeCore.client.system.BaseClientSystem import BaseClientSystem
from jufufuBlockFrameAniScript.CodeCore.utils.eventWrapper import EngineEvent, AddonEvent
from jufufuBlockFrameAniScript.modCommon import modConfig
from jufufuBlockFrameAniScript.modClient.ui.uiDef import UIDef
from jufufuBlockFrameAniScript.modCommon.cfg.items import labelConfig
from jufufuBlockFrameAniScript.modCommon.cfg.blocks import facePosConfig
from jufufuBlockFrameAniScript.CodeCore.client import engineApiGac
from jufufuBlockFrameAniScript.CodeCore.client.api import clientApiMgr
from jufufuBlockFrameAniScript.modClient.manager.singletonGac import Instance
import mod.client.extraClientApi as clientApi
from mod_log import logger
import math

compFactory = clientApi.GetEngineCompFactory()
minecraftEnum = clientApi.GetMinecraftEnum()
EntityTypeEnum = clientApi.GetMinecraftEnum().EntityType


class SelectClientSystem(BaseClientSystem):
	def __init__(self, namespace, systemName):
		super(SelectClientSystem, self).__init__(namespace, systemName)
		# 检测手上是否有添加物品
		self._nowHandleItem = None
		self._canAddLabel = False
		# UI
		self._createBtnObj = None
		# 绘制
		self._lineBoxObj = None
		# status
		self._nowSelectPos = None
		self._selectPos1 = None
		self._selectPos2 = None

		self._time = 0

	@EngineEvent()
	def OnCarriedNewItemChangedClientEvent(self, args):
		newItemName = args['itemDict']['newItemName']
		if self._nowHandleItem == newItemName:
			return
		self._nowHandleItem = newItemName
		if labelConfig.IsCanAddLabel(newItemName):
			self.HasStartAdd()
		else:
			self.HasStopAdd()

	def HasStartAdd(self):
		self._canAddLabel = True
		if not self._createBtnObj:
			btnObj = self.CreateUI(UIDef.UI_jufufuCreateBtn, {"isHud": 1})
			if btnObj: 
				self._createBtnObj = btnObj
		if not self._lineBoxObj:
			self._lineBoxObj = self.CreateLineBox((0, 0, 0), (0, 0, 0), (1, 1, 1))

	def HasStopAdd(self):
		self._canAddLabel = True
		if self._createBtnObj:
			self._createBtnObj.SetRemove()
			self._createBtnObj = None
		if self._lineBoxObj:
			self._lineBoxObj.Destroy()
			self._lineBoxObj = None
			self._selectPos1 = None
			self._selectPos2 = None

	def Update(self):
		self._time += 1
		if self._time % 1 == 0:
			self._time = 0
			if self._canAddLabel and self._lineBoxObj:
				self._nowSelectPos = self.GetSelectPos(4)
				if self._selectPos1:
					if not self._selectPos2:
						self._lineBoxObj.UpdateLineBoxEndPos(self._nowSelectPos)
				else:
					self._lineBoxObj.UpdateLineBoxStartPos(self._nowSelectPos)
					self._lineBoxObj.UpdateLineBoxEndPos(self._nowSelectPos)

	def CreateLineBox(self, startPos, endPos, color):
		"""通过线拼出的Box。支持设置起始点与终点"""
		if self._lineBoxObj:
			return self._lineBoxObj
		return LineBoxClass(startPos, endPos, color)
		
	# region 监听
	@AddonEvent(modConfig.ModNameSpace, modConfig.ClientSystemEnum.ClientSystem)
	def CreateBtnClicked(self, args):
		if self._nowSelectPos:
			if not self._selectPos1:
				self._selectPos1 = self._nowSelectPos
				self._lineBoxObj.UpdateLineBoxStartPos(self._selectPos1)
				self.BroadcastEvent("SetCreateBtnText", {"text": "选择第二点"})
				self.SendMsgToServer("test123", {"pos": self._selectPos1})
			elif self._selectPos1 and not self._selectPos2:
				self._selectPos2 = self._nowSelectPos
				self._lineBoxObj.UpdateLineBoxEndPos(self._selectPos2)
				self.SendMsgToServer("test123", {"pos": self._selectPos2})
				self.BroadcastEvent("SetCreateBtnText", {"text": "创建"})
			else:
				Instance.mUIManager.PushUI(UIDef.UI_JufufuTSet)

	def RemoveUI(self, uiObj):
		if uiObj:
			uiObj.SetRemove()

	# region 方法
	def CreateUI(self, uiData, createParams=None):
		uiKey = uiData["ui_key"]
		ui = clientApi.CreateUI(modConfig.ModNameSpace, uiKey, createParams)
		if ui is None:
			logger.error("========create UI Failed %s===========", str(uiData['ui_namespace']))
			return
		hasattr(ui, "InitScreen") and ui.InitScreen()
		return ui
	
	def GetFaceBlockCenter(self, surface = False):
		"""获取 PickFacing 到的方块坐标。surface为True时返回方块表面坐标。None代表没有指向方块"""
		pickData = compFactory.CreateCamera(self.mLevelId).PickFacing()
		if pickData['type'] == 'Block':
			x, y, z, face = pickData['x'],pickData['y'],pickData['z'], pickData['face']
			if surface:
				# faceDict = {0: (0.5, -0.01, 0.5), 1: (0.5, 1.01, 0.5), 2: (0.5, 0.5, -0.01),
				# 2: (0.5, 0.5, 1.01), 2: (-0.01, 0.5, 0.5), 2: (1.01, 0.5, 0.5)}
				# if face in faceDict:
				# 	offsetPos = faceDict[face]
				# 	x += offsetPos[0]
				# 	y += offsetPos[1]
				# 	z += offsetPos[2]
				return (pickData['hitPosX'], pickData['hitPosY'], pickData['hitPosZ'])
			return (x, y, z)
		return None
	
	def GetSelectPos(self, offset):
		"""获取选择点坐标 指向方块时是方块的坐标。offset代表没选中方块时在玩家指向的几格位置作为选择点"""
		blockPos = self.GetFaceBlockCenter(True)
		if blockPos:
			return blockPos
		else:
			mDir = clientApi.GetDirFromRot(compFactory.CreateRot(self.mPlayerId).GetRot())
			engineApiGac.GetEntityPos(self.mPlayerId)
			x, y, z = engineApiGac.GetEntityPos(self.mPlayerId)
			dx, dy, dz = mDir
			# 计算精确坐标
			targetX = x + offset * dx
			targetY = y + offset * dy
			targetZ = z + offset * dz
			return (targetX, targetY, targetZ)
		
# region [Class]线创建Box
class LineBoxClass(object):
	"""
	使用 AddLineShape 绘制 12 条线来模拟一个 Box。
	startPos 与 endPos 为对角线两点（三维坐标）。
	"""
	def __init__(self, startPos, endPos, color):
		self.mLevelId = clientApi.GetLevelId()
		self.start = startPos
		self.end = endPos
		self.color = color
		# 12条线段
		self.lines = []
		self._create_lines()
	# Box 创建
	def _create_lines(self):
		sx, sy, sz = self.start
		ex, ey, ez = self.end
		# 计算 8 个角点
		p000 = (sx, sy, sz)
		p001 = (sx, sy, ez)
		p010 = (sx, ey, sz)
		p011 = (sx, ey, ez)
		p100 = (ex, sy, sz)
		p101 = (ex, sy, ez)
		p110 = (ex, ey, sz)
		p111 = (ex, ey, ez)
		# 12 条边
		edges = [
			(p000, p001), (p000, p010), (p001, p011), (p010, p011),   # 左面
			(p100, p101), (p100, p110), (p101, p111), (p110, p111),   # 右面
			(p000, p100), (p001, p101), (p010, p110), (p011, p111),   # 中间连接
		]
		# 创建线段对象
		for start, end in edges:
			lineObj = compFactory.CreateDrawing(self.mLevelId).AddLineShape(start, end, self.color)
			self.lines.append(lineObj)
	# 更新坐标（重算）
	def _update_all_lines(self):
		"""根据 self.start 和 self.end 重新设置 12 条线坐标"""
		if not self.start:
			logger.error("没有起始点坐标")
			return 
		if not self.end:
			logger.error("没有终点坐标")
			return
		sx, sy, sz = self.start
		ex, ey, ez = self.end
		# 更新角点
		p000 = (sx, sy, sz)
		p001 = (sx, sy, ez)
		p010 = (sx, ey, sz)
		p011 = (sx, ey, ez)
		p100 = (ex, sy, sz)
		p101 = (ex, sy, ez)
		p110 = (ex, ey, sz)
		p111 = (ex, ey, ez)
		# 设置颜色
		greenColor, redColor, buleColor, whiteColor = (0, 1, 0), (1, 0, 0), (0, 0, 1), (1, 1, 1)
		edges = [
			(p000, p001, buleColor), (p000, p010, greenColor), (p001, p011, whiteColor), (p010, p011, whiteColor),
			(p100, p101, whiteColor), (p100, p110, whiteColor), (p101, p111, whiteColor), (p110, p111, whiteColor),
			(p000, p100, redColor), (p001, p101, whiteColor), (p010, p110, whiteColor), (p011, p111, whiteColor),
		]
		# 对应更新 12 条线的位置
		for lineObj, (newStart, newEnd, color) in zip(self.lines, edges):
			if lineObj:
				lineObj.SetPos(newStart)
				lineObj.SetEndPos(newEnd)
				lineObj.SetColor(color)
		
	# 更新 startPos / endPos
	def UpdateLineBoxStartPos(self, newStartPos):
		self.start = newStartPos
		self._update_all_lines()

	def UpdateLineBoxEndPos(self, newEndPos):
		self.end = newEndPos
		self._update_all_lines()

	# 对外销毁接口
	def Destroy(self):
		if self.lines:
			for lineObj in self.lines:
				lineObj.Remove()

