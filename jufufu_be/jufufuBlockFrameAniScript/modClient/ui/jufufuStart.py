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


class JufufuStart(ModBaseUI):
	def __init__(self, namespace, name, param):
		super(JufufuStart, self).__init__(namespace, name, param)
		self._param = param
		self._mainPanel = "/main_panel"
		self._btnPath = {
			"startBtn": self._mainPanel + "/startBtn"
		}
		self._btnDic = {}
		self._textPath = {
			"startBtnText": self._mainPanel + "/startBtn/button_label"
		}
		self._textDic = {}

	def Create(self):
		super(JufufuStart, self).Create()
		for key, path in self._btnPath.items():
			self._btnDic[key] = self.GetBaseUIControl(path).asButton()
			clientApiMgr.SetBtnTouchUpCallback(self._btnDic[key], self.OnBtnClicked, {"key": key})
		for key, path in self._textPath.items():
			self._textDic[key] = self.GetBaseUIControl(path).asLabel()
		self.UIInit()

	def UIInit(self):
		pass

	def Update(self):
		pass

	def OnBtnClicked(self, args):
		self.BroadcastEvent("StartBtnClicked", args)
