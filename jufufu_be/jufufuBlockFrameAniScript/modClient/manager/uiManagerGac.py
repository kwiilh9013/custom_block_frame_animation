# -*- encoding: utf-8 -*-
import mod.client.extraClientApi as clientApi
from jufufuBlockFrameAniScript.modCommon.manager.commonMgr import CommonManager
from jufufuBlockFrameAniScript.modCommon import modConfig
from jufufuBlockFrameAniScript.modClient.ui.uiDef import UIDef
from mod_log import logger


class UIManagerGac(CommonManager):
	def __init__(self, system):
		super(UIManagerGac, self).__init__(system)
		self.mRegisterFlag = {}
		self.mUIDict = {}

	def UiInitFinished(self, args):
		self.Clear()
		self.RegisterUI(UIDef.UI_JufufuTSet)
		self.RegisterUI(UIDef.UI_jufufuCreateBtn)

	def RegisterUI(self, uiData):
		if not self.mRegisterFlag.get(uiData["ui_key"], False):
			_uiKey = uiData["ui_key"]
			self.mRegisterFlag[_uiKey] = clientApi.RegisterUI(modConfig.ModNameSpace, _uiKey, uiData["ui_cls_path"], uiData["ui_namespace"])

	def CreateUI(self, uiData, createParams=None):
		uiKey = uiData["ui_key"]
		ui = clientApi.CreateUI(modConfig.ModNameSpace, uiKey, createParams)
		if ui is None:
			logger.error("========create UI Failed %s===========", str(uiData['ui_namespace']))
			return
		hasattr(ui, "InitScreen") and ui.InitScreen()
		self.mUIDict[uiKey] = ui
		return ui

	def PushUI(self, uiData, createParams=None):
		"""
		通过pushscreen的方式创建打开ui，每次打开ui都会将ui类初始化一遍
		:param uiData:
		:return:
		"""
		uiKey = uiData['ui_key']
		ui = clientApi.PushScreen(modConfig.ModNameSpace, uiKey, createParams)
		if not ui:
			logger.error('==== %s ====' % '"push UI failed": %s' % uiData['ui_namespace'])
			return
		return ui

	def PopUI(self):
		"""
		通过popscreen的方式关闭由pushscreen打开的ui
		:return:
		"""
		return clientApi.PopScreen()

	def GetTopUI(self):
		return clientApi.GetTopUI()

	def GetUIFromDict(self, uiKey):
		return self.mUIDict.get(uiKey, None)

	def GetUI(self, uiDef):
		return self.GetUIByKey(uiDef['ui_key'])

	def GetUIByKey(self, uiKey):
		if uiKey not in self.mRegisterFlag:
			return None
		ui = self.mUIDict.get(uiKey)
		if ui:
			if not ui.removed:
				return ui
			else:
				return None
		return clientApi.GetUI(modConfig.ModNameSpace, uiKey)

	def HasUI(self, uiKey):
		return uiKey in self.mUIDict

	def Clear(self):
		for node in self.mUIDict.values():
			node.Destroy()
		self.mUIDict.clear()
		self.mRegisterFlag.clear()
