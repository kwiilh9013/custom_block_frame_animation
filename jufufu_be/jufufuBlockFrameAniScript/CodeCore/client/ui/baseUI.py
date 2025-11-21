# -*- encoding: utf-8 -*-
import mod.client.extraClientApi as clientApi
from jufufuBlockFrameAniScript.CodeCore.client.ui.utils import uiUtils
from mod_log import logger

from jufufuBlockFrameAniScript.CodeCore.common.log.logMetaClass import LogMetaClass


view_binder = clientApi.GetViewBinderCls()
view_request = clientApi.GetViewViewRequestCls()
screen_node = clientApi.GetScreenNodeCls()


class BaseUI(screen_node):
    __metaclass__ = LogMetaClass

    def __init__(self, namespace, name, param):
        screen_node.__init__(self, namespace, name, param)
        self.mNamespace = namespace
        self.mLevelId = clientApi.GetLevelId()
        self.mPlayerId = clientApi.GetLocalPlayerId()
        self.mPathVisible = {}
        self.mWidgetList = []

    def Destroy(self):
        for widget in self.mWidgetList:
            widget.Destroy()
        self.mPathVisible.clear()

    def InitScreen(self):
        pass

    def SetControlVisible(self, path, visible):
        """
        设置控件是否可见
        :param str path 控件路径
        :param bool visible 是否可见
        """
        if self.mPathVisible.get(path, None) == visible:
            return
        self.mPathVisible[path] = visible
        self.SetVisible(path, visible)

    def GetControlVisible(self, path):
        if path not in self.mPathVisible:
            logger.info("控件路径有误 或未设置过该路径的UI %s" + path)
            return False
        return self.mPathVisible[path]

    def GetRealScrollView(self, componentPath):
        path = componentPath + "/scroll_touch/scroll_view"
        childList = self.GetChildrenName(path)
        if childList and len(self.GetChildrenName(path)) > 0:
            return path + "/panel/background_and_viewport/scrolling_view_port/scrolling_content"
        path = componentPath + "/scroll_mouse/scroll_view"
        childList = self.GetChildrenName(path)
        if childList and len(self.GetChildrenName(path)) > 0:
            return path + "/stack_panel/background_and_viewport/scrolling_view_port/scrolling_content"
        return ""

    def RegisterButton(self, buttonPath, funcDict, parm={"isSwallow": True}):
        """
        注册按钮，主要是设置按钮的回调函数
        :param buttonPath: 按钮路径
        :param funcDict: 回调函数(up,down,cancel,move)
        :param parm:绑定参数
        :return:
        """
        buttonUIControl = self.GetBaseUIControl(buttonPath).asButton()
        if not buttonUIControl:
            logger.info("按钮注册失败")
            return
        buttonUIControl.AddTouchEventParams(parm)
        funcDict.get('up') and buttonUIControl.SetButtonTouchUpCallback(funcDict['up'])
        funcDict.get('down', True) and buttonUIControl.SetButtonTouchDownCallback(
            funcDict.get('down', self.OnButtonNormalDown))
        funcDict.get('cancel') and buttonUIControl.SetButtonTouchCancelCallback(funcDict['cancel'])
        funcDict.get('move') and buttonUIControl.SetButtonTouchMoveCallback(funcDict['move'])

    @uiUtils.button_touch("down")
    def OnButtonNormalDown(self, args):
        pass

    def SetButtonAlpha(self, buttonPath, alpha):
        self.GetBaseUIControl(buttonPath).GetChildByName('pressed').asImage().SetAlpha(alpha)
        self.GetBaseUIControl(buttonPath).GetChildByName('default').asImage().SetAlpha(alpha)
        self.GetBaseUIControl(buttonPath).GetChildByName('hover').asImage().SetAlpha(alpha)

    def SetButtonImage(self, buttonPath, texture):
        self.GetBaseUIControl(buttonPath).GetChildByName('pressed').asImage().SetSprite(texture)
        self.GetBaseUIControl(buttonPath).GetChildByName('default').asImage().SetSprite(texture)
        self.GetBaseUIControl(buttonPath).GetChildByName('hover').asImage().SetSprite(texture)

    def GetBaseUIControl(self, controlPath):
        basePath = "/variables_button_mappings_and_controls/safezone_screen_matrix/inner_matrix/safezone_screen_panel/root_screen_panel"
        baseControl = super(BaseUI, self).GetBaseUIControl(controlPath)
        if not baseControl:
            return super(BaseUI, self).GetBaseUIControl(basePath + controlPath)
        return baseControl

    def AddWidgetObj(self, widgetObj):
        self.mWidgetList.append(widgetObj)