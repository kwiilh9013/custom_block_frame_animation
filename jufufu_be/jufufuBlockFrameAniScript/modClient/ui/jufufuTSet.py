# -*- coding: utf-8 -*-
from jufufuBlockFrameAniScript.modClient.ui.baseUI import ModBaseUI
from jufufuBlockFrameAniScript.modCommon import modConfig
import mod.client.extraClientApi as clientApi
from jufufuBlockFrameAniScript.CodeCore.common.api.commonApiMgr import DeepCopy
from jufufuBlockFrameAniScript.CodeCore.client import engineApiGac
from jufufuBlockFrameAniScript.CodeCore.common.api import itemApi
from jufufuBlockFrameAniScript.CodeCore.client.api import clientApiMgr
from jufufuBlockFrameAniScript.CodeCore.client.ui.utils import uiUtils
from jufufuBlockFrameAniScript.CodeCore.utils.mathUtils import MathUtils
from jufufuBlockFrameAniScript.CodeCore.common.system.commonEventRegister import CommonEventRegister
from jufufuBlockFrameAniScript.CodeCore.utils.eventWrapper import EngineEvent, AddonEvent
from jufufuBlockFrameAniScript.modClient.ui.uiDef import UIDef
import math
import time
from mod_log import logger

compFactory = clientApi.GetEngineCompFactory()
minecraftEnum = clientApi.GetMinecraftEnum()
safePath0 = '/variables_button_mappings_and_controls/safezone_screen_matrix/inner_matrix'
safePath = safePath0+'/safezone_screen_panel/root_screen_panel'


class JufufuTSet(ModBaseUI):
	def __init__(self, namespace, name, param):
		super(JufufuTSet, self).__init__(namespace, name, param)
		self._mainPanelPath = "/main_panel"
		self._rightPanelPath = self._mainPanelPath + "/right_panel"
		self._btnPath = {
			"closeBtn": self._rightPanelPath + "/close_panel/close_btn",
		}
		self._btnDic = {}

	def Create(self):
		super(JufufuTSet, self).Create()
		for key, path in self._btnPath.items():
			self._btnDic[key] = self.GetBaseUIControl(path).asButton()
			clientApiMgr.SetBtnTouchUpCallback(self._btnDic[key], self.OnBtnClicked, {"key": key})
		self.UIInit()

	def UIInit(self):
		pass

	def Update(self):
		pass

	def OnBtnClicked(self, args):
		AddTouchEventParams = args["AddTouchEventParams"]
		key = AddTouchEventParams.get("key", "")
		if key == "closeBtn":
			clientApi.PopScreen()
