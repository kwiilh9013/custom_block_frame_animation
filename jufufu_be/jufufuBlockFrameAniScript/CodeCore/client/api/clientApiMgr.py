# -*- encoding: utf-8 -*-
"""
客户端的通用方法
"""
import mod.client.extraClientApi as clientApi
from jufufuBlockFrameAniScript.CodeCore.common.api import commonApiMgr, itemApi, recipesApi
from jufufuBlockFrameAniScript.CodeCore.client import engineApiGac
compFactory = clientApi.GetEngineCompFactory()
minecraftEnum = clientApi.GetMinecraftEnum()


# region 变量
# 地图id
levelId = clientApi.GetLevelId()
# endregion


# region 属性

_PlatformId = None


def IsWinPlatform():
    """判断是否是电脑平台"""
    global _PlatformId
    if _PlatformId is None:
        _PlatformId = clientApi.GetPlatform()
    return _PlatformId == 0

# endregion


# region 实体属性
def GetCurrentDimension():
    """获取客户端当前的维度"""
    gameComp = compFactory.CreateGame(levelId)
    return gameComp.GetCurrentDimension()


def GetEntityCustomName(entityId):
    """获取实体自定义名字，包括玩家名"""
    nameComp = compFactory.CreateName(entityId)
    return nameComp.GetName()


def GetEntityName(engineTypeStr):
    """获取实体lang命名"""
    gameComp = compFactory.CreateGame(levelId)
    # 原版生物需去掉minecraft:前缀
    return gameComp.GetChinese("entity.%s.name" % engineTypeStr.replace("minecraft:", "")) or ""


def GetEffectText(effectId, level, duration):
    """获取buff显示文字，包括等级、持续时间，减益buff红色"""
    return commonApiMgr.GetEffectText(compFactory, levelId, effectId, level, duration)


# endregion


# region 方块、物品相关
def GetPlayerCarriedItem(playerId):
    """获取玩家当前手持物品"""
    itemComp = compFactory.CreateItem(playerId)
    return itemComp.GetCarriedItem(True)


def GetPlayerInventoryItemList(playerId):
    """获取玩家背包物品，返回list=[{item}]"""
    # 获取本地玩家的背包物品
    itemComp = compFactory.CreateItem(playerId)
    # 格式：[ {item}, None, {item} ]
    itemListDict = itemComp.GetPlayerAllItems(minecraftEnum.ItemPosType.INVENTORY, True)
    return itemListDict


def GetPlayerInventoryItems(playerId):
    """获取玩家背包物品，返回dict={slot: item}"""
    # 获取本地玩家的背包物品
    itemListDict = GetPlayerInventoryItemList(playerId)
    # 改成slot格式
    itemDict = {}
    slot = 0
    for item in itemListDict:
        if item:
            itemDict[slot] = item
        slot += 1
    return itemDict


def GetPlayerInventoryItemsCount(playerId):
    """获取玩家背包所有物品数量，返回dict={(name, aux): count}"""
    # 获取本地玩家的背包物品
    itemListDict = GetPlayerInventoryItemList(playerId)
    # 统计数量
    itemDict = {}
    for item in itemListDict:
        if item:
            key = (item.get("newItemName"), item.get("newAuxValue", 0))
            itemDict[key] = itemDict.get(key, 0) + item.get("count", 0)
    return itemDict


def GetItemRecipes(itemName, aux, tag=None):
    """获取物品的合成配方（合成材料）"""
    return recipesApi.GetItemRecipes(compFactory, levelId, itemName, aux, tag)


def GetItemMaxDurability(itemName):
    """获取物品的最大耐久"""
    return itemApi.GetItemMaxDurability(compFactory, levelId, itemName)


def GetItemHoverText(item):
    """获取物品的名字文本，包括附魔、攻击力等"""
    # GetItemFormattedHoverText = 包括附魔、攻击力文字（类似背包中选中时显示的文字）
    if item:
        itemComp = compFactory.CreateItem(levelId)
        itemName = item.get("newItemName")
        aux = item.get("newAuxValue", 0)
        userData = item.get("userData")
        return itemComp.GetItemFormattedHoverText(itemName, aux, userData=userData)
    return ""


def GetItemHoverName(item):
    """获取物品的名字文本，仅名字"""
    if item:
        itemComp = compFactory.CreateItem(levelId)
        itemName = item.get("newItemName")
        aux = item.get("newAuxValue", 0)
        userData = item.get("userData")
        return itemComp.GetItemHoverName(itemName, aux, userData=userData)
    return ""

# endregion


# region 音效
def PlayCustomMusic(soundName, pos, volume=1, pitch=1, loop=False, entityId=None):
    """播放声音"""
    audioComp = compFactory.CreateCustomAudio(levelId)
    soundId = audioComp.PlayCustomMusic(soundName, pos, volume, pitch, loop, entityId)
    return soundId


def StopCustomMusicById(soundId, fadeOutTime=0):
    """停止声音"""
    audioComp = compFactory.CreateCustomAudio(levelId)
    return audioComp.StopCustomMusicById(soundId, fadeOutTime)
# endregion


# region 特效相关
def CreateMicroParticle(particleName, pos, rot=None, delayTime=None):
    """创建原版粒子效果"""
    particleComp = compFactory.CreateParticleSystem(levelId)
    parId = particleComp.Create(particleName, pos)
    if rot:
        particleComp.SetRot(parId, rot)
    # 延迟销毁
    if delayTime:
        engineApiGac.AddTimer(delayTime, particleComp.Remove, parId)
    return parId


def CreateMicroParticleBindEntity(particleName, entityId, boneName="body", offset=(0, 0, 0), rotation=(0, 0, 0), delayTime=None):
    """创建原版粒子效果，绑定实体"""
    particleComp = compFactory.CreateParticleSystem(levelId)
    parId = particleComp.Create(particleName)
    particleComp.BindEntity(parId, entityId, boneName, offset=offset, rotation=rotation)
    # 延迟销毁
    if delayTime:
        engineApiGac.AddTimer(delayTime, particleComp.Remove, parId)
    return parId


def SetMicroParticleVariable(parId, variable, value):
    """设置原版粒子的variable值"""
    particleComp = compFactory.CreateParticleSystem(levelId)
    particleComp.SetVariable(parId, variable, value)
    pass


def ResetMicroParticleParam(parId, pos=None, rot=None):
    """重置原版粒子的属性：位置、角度"""
    particleComp = compFactory.CreateParticleSystem(levelId)
    if pos:
        particleComp.SetPos(parId, pos)
    if rot:
        particleComp.SetRot(parId, rot)
    # 重启粒子
    particleComp.Replay(parId)
    pass


def RemoveMicroParticle(parId):
    """删除原版粒子"""
    particleComp = compFactory.CreateParticleSystem(levelId)
    particleComp.Remove(parId)
    pass


def SetMicroParticlePos(parId, pos):
    """设置原版粒子位置"""
    particleComp = compFactory.CreateParticleSystem(levelId)
    particleComp.SetPos(parId, pos)
    pass


def IsExistByMicroParticle(parId):
    """判断原版粒子是否存在"""
    particleComp = compFactory.CreateParticleSystem(levelId)
    return particleComp.Exist(parId)
# endregion

# region UI相关

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

def SetButtonText(buttonObj, text):
    """设置按钮文字"""
    textObj = buttonObj.GetChildByPath("/button_label").asLabel()
    textObj.SetText(text)
    pass

def SetButtonTextColor(buttonObj, color):
    """设置按钮文字颜色"""
    textObj = buttonObj.GetChildByPath("/button_label").asLabel()
    textObj.SetTextColor(color)
    pass

def SetBtnTouchDonwUpCallback(btnObj, downCallback, upCallback, clickParam=None):
    """
    设置按钮【按下、松开】回调函数，适用按下持续执行松开停止的逻辑
    :param btnObj: 按钮对象
    :param downCallback: 按下回调函数
    :param clickParam dict: 事件传递的参数， isSwallow默认=True
    :param upCallback: 松开回调函数
    """
    # 如果没有加isSwallow，则手动加一下，默认为True
    if not clickParam:
        clickParam = {"isSwallow": True}
    elif clickParam.get("isSwallow") is None:
        clickParam["isSwallow"] = True
    btnObj.AddTouchEventParams(clickParam)
    # 按下
    btnObj.SetButtonTouchDownCallback(downCallback)
    # 松开的各种情况
    btnObj.SetButtonTouchUpCallback(upCallback)
    btnObj.SetButtonTouchCancelCallback(upCallback)
    btnObj.SetButtonScreenExitCallback(upCallback)
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


def SetBtnTouchDownCallback(btnObj, downCallback, clickParam=None):
    """
    设置按钮【按下】回调函数
    :param btnObj: 按钮对象
    :param upCallback: 松开回调函数
    :param clickParam dict: 事件传递的参数， isSwallow默认=True
    """
    # 如果没有加isSwallow，则手动加一下，默认为True
    if not clickParam:
        clickParam = {"isSwallow": True}
    elif clickParam.get("isSwallow") is None:
        clickParam["isSwallow"] = True
    btnObj.AddTouchEventParams(clickParam)
    # 松开
    btnObj.SetButtonTouchDownCallback(downCallback)
    pass

def SetBtnTouchUpCallback(btnObj, upCallback, clickParam=None):
    """
    设置按钮【松开】回调函数
    :param btnObj: 按钮对象
    :param upCallback: 松开回调函数
    :param clickParam dict: 事件传递的参数， isSwallow默认=True
    """
    # 如果没有加isSwallow，则手动加一下，默认为True
    if not clickParam:
        clickParam = {"isSwallow": True}
    elif clickParam.get("isSwallow") is None:
        clickParam["isSwallow"] = True
    btnObj.AddTouchEventParams(clickParam)
    # 松开
    btnObj.SetButtonTouchUpCallback(upCallback)
    pass


def GetDurabilityColor(ratio):
    """根据耐久度获取颜色，用于耐久进度条的显示"""
    # ratio = durability / maxDurability
    return (1 - ratio, ratio, 0)

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


