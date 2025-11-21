# -*- coding: utf-8 -*-
from functools import wraps
import mod.client.extraClientApi as clientApi
# region UI相关

TouchScrollViewPath = "/scroll_touch/scroll_view/panel/background_and_viewport/scrolling_view_port/scrolling_content"


def IsScreenUI():
    """是否处于主界面UI"""
    return clientApi.GetTopUI() == "hud_screen"


def SetUIVisible(uiObj, state):
    """
    设置UI显示状态
    :param state(bool): UI显示状态
    """
    # 频繁SetVisible，容易卡顿，所以需要减少设置
    if uiObj and uiObj.GetVisible() is not state:
        uiObj.SetVisible(state)
    pass


def SetButtonImage(buttonObj, texture, pressTexture=None, hoverTexture=None):
    """设置按钮图片"""
    if pressTexture is None:
        pressTexture = texture
    if hoverTexture is None:
        hoverTexture = pressTexture
    buttonObj.GetChildByPath("/default").asImage().SetSprite(texture)
    buttonObj.GetChildByPath("/pressed").asImage().SetSprite(pressTexture)
    buttonObj.GetChildByPath("/hover").asImage().SetSprite(hoverTexture)
    pass


def SetButtonGray(buttonObj, state):
    """设置按钮为灰色"""
    buttonObj.GetChildByPath("/default").asImage().SetSpriteGray(state)
    buttonObj.GetChildByPath("/pressed").asImage().SetSpriteGray(state)
    buttonObj.GetChildByPath("/hover").asImage().SetSpriteGray(state)
    pass


def SetButtonColor(buttonObj, defaultColor, hoverColor=None, pressColor=None):
    """设置按钮颜色"""
    if hoverColor is None:
        hoverColor = defaultColor
    if pressColor is None:
        pressColor = hoverColor
    buttonObj.GetChildByPath("/default").asImage().SetSpriteColor(defaultColor)
    buttonObj.GetChildByPath("/hover").asImage().SetSpriteColor(hoverColor)
    buttonObj.GetChildByPath("/pressed").asImage().SetSpriteColor(pressColor)
    pass


# 创建UI按钮
def UICreateBtn(uiInstance, btnDict, btnKey, path, param=None, upFunc=None, downFunc=None, moveFunc=None):
    if param is None:
        param = {"isSwallow": True, "type": btnKey}
    if type(btnDict) != dict:
        btnDict = {}
    if type(btnKey) != str:
        return
    btnDict.update({btnKey: uiInstance.GetBaseUIControl(path).asButton()})
    btnDict[btnKey].AddTouchEventParams(param)
    if upFunc is not None:
        btnDict[btnKey].SetButtonTouchUpCallback(upFunc)
    if downFunc is not None:
        btnDict[btnKey].SetButtonTouchDownCallback(downFunc)
    if moveFunc is not None:
        btnDict[btnKey].SetButtonTouchMoveCallback(moveFunc)


# 给某个面板绑定移动
def UICreateMoveObj(uiInstance, moveArgs, moveMark, panelPath, safeZoomPath=None):
    if not moveArgs: return
    if type(moveArgs) != dict: return
    if "TouchPosX" not in moveArgs: return
    posX = moveArgs['TouchPosX']
    posY = moveArgs['TouchPosY']
    mark = getattr(uiInstance, moveMark)
    if mark:
        deltaX = posX - mark[0]
        deltaY = posY - mark[1]
        panel = uiInstance.GetBaseUIControl(panelPath)
        panelX, panelY = panel.GetSize()
        nowPos = panel.GetPosition()
        safeX = nowPos[0] + deltaX
        safeY = nowPos[1] + deltaY
        if safeZoomPath:
            safePanel = uiInstance.GetBaseUIControl(safeZoomPath)
            maxX, maxY = safePanel.GetSize()
            panelPosX, panelPosY = safePanel.GetPosition()
            safeX = max(min(nowPos[0] + deltaX, maxX - panelX + panelPosX), 1 + panelPosX)
            safeY = max(min(nowPos[1] + deltaY, maxY - panelY + panelPosY), 1 + panelPosY)
        panel.SetPosition((safeX, safeY))
    setattr(uiInstance, moveMark, (posX, posY))


def GetScrollViewChildPath(viewObj):
    """
    获取scroll_view的子控件路径
    :param viewObj: scroll_view对象
    """
    # 准星模式和触屏模式下，scroll_view的子控件路径不一样
    childObj = viewObj.GetChildByPath("/scroll_touch/scroll_view")
    if childObj:
        return "/scroll_touch/scroll_view/panel/background_and_viewport/scrolling_view_port/scrolling_content"
    childObj = viewObj.GetChildByPath("/scroll_mouse/scroll_view")
    if childObj:
        return "/scroll_mouse/scroll_view/stack_panel/background_and_viewport/scrolling_view_port/scrolling_content"
    return ""


def GetDurabilityColor(ratio):
    """根据耐久度获取颜色，用于耐久进度条的显示"""
    # ratio = durability / maxDurability
    return 1 - ratio, ratio, 0


def GetUIPosition(parentUIObj, path):
    """
    获取控件相对某个父控件的相对坐标
    :param uiCls: 父控件对象
    :param path: 相对父控件的路径
    :return: 坐标元组(x,y)
    """
    pos = [0, 0]
    splitPath = path.split("/")
    for path in splitPath:
        if path:
            # 获取下一层ui的对象
            childObj = parentUIObj.GetChildByName(path)
            if childObj:
                # 获取位置
                cpos = childObj.GetPosition()
                pos[0] += cpos[0]
                pos[1] += cpos[1]
                # 将父控件换成子控件，继续获取下一层的坐标
                parentUIObj = childObj
    return tuple(pos)

# endregion

def touch_filter(touchType):
    def touchFilter(func):
        @wraps(func)
        def decorated(*args, **kwargs):
            touchEventEnum = clientApi.GetMinecraftEnum().TouchEvent
            touchEvent = args[1]["TouchEvent"]
            if touchType == "up":
                if touchEvent == touchEventEnum.TouchUp:
                    value = func(*args, **kwargs)
                    return value
            if touchType == "down":
                if touchEvent == touchEventEnum.TouchDown:
                    value = func(*args, **kwargs)
                    return value
            if touchType == "cancel":
                if touchEvent == touchEventEnum.TouchCancel:
                    value = func(*args, **kwargs)
                    return value
            if touchType == "move":
                if touchEvent == touchEventEnum.TouchMove:
                    value = func(*args, **kwargs)
                    return value

        return decorated

    return touchFilter


# 按钮点击时透明度变化
def button_touch(touchType):
    def touchFilter(func):
        def wrapper(*args, **kwargs):
            if touchType == 'down':
                uiNode = args[0]
                buttonPath = args[1]['ButtonPath']
                uiNode and uiNode.SetAlpha("{}/pressed".format(buttonPath), 0.5)
            elif touchType == 'up':
                pass
            value = func(*args, **kwargs)
            return value

        return wrapper

    return touchFilter
