from jufufuBlockFrameAniScript.CodeCore.common.log.logMetaClass import LogMetaClass
import mod.client.extraClientApi as clientApi

screen_node = clientApi.GetScreenNodeCls()

class BaseWidget(object):
	__metaclass__ = LogMetaClass

	def __init__(self, baseUI, path):
		self._basePath = path
		self._baseUI = baseUI
		self._baseUI.AddWidgetObj(self)

	def Destroy(self):
		del self
		pass

	def GetBaseUIControl(self, controlPath):
		basePath = self._basePath
		return self._baseUI.GetBaseUIControl(basePath + controlPath)

	def Clone(self, path, parentPath, name):
		path = self._basePath + path
		parentPath = self._basePath + parentPath
		return self._baseUI.Clone(path, parentPath, name)
	
	def SetUIVisible(self, uiControl, visible):
		if uiControl and uiControl.GetVisible() != visible:
			uiControl.SetVisible(visible)
		pass
