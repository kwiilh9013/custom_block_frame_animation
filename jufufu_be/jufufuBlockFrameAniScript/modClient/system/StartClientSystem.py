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


class StartClientSystem(BaseClientSystem):
	def __init__(self, namespace, systemName):
		super(StartClientSystem, self).__init__(namespace, systemName)
		# 检测手上是否有添加物品
		self._nowHandleItem = None
		self._canAddLabel = False
		# UI
		self._startBtnObj = None
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
		if newItemName == "minecraft:stick":
			self.CanStartUI()
		else:
			self.HasStopUI()

	def CanStartUI(self):
		self._canAddLabel = True
		if not self._startBtnObj:
			btnObj = self.CreateUI(UIDef.UI_JufufuStart, {"isHud": 1})
			if btnObj: 
				self._startBtnObj = btnObj

	def HasStopUI(self):
		self._canAddLabel = True
		if self._startBtnObj:
			self._startBtnObj.SetRemove()
			self._startBtnObj = None

	def Update(self):
		self._time += 1
		if self._time % 1 == 0:
			self._time = 0
		
	# region 监听
	@AddonEvent(modConfig.ModNameSpace, modConfig.ClientSystemEnum.ClientSystem)
	def StartBtnClicked(self, args):
		Instance.mUIManager.PushUI(UIDef.UI_JufufuMain)

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

