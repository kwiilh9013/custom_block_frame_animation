# -*- encoding: utf-8 -*-
"""
服务端的通用方法
"""
import mod.server.extraServerApi as serverApi
from jufufuBlockFrameAniScript.CodeCore.common.api import commonApiMgr, itemApi

compFactory = serverApi.GetEngineCompFactory()
minecraftEnum = serverApi.GetMinecraftEnum()

# region 变量
# 地图id
levelId = serverApi.GetLevelId()

# 方块挖掘数据：工具类型、挖掘等级
_BlockDigCache = {}

# 方块硬度数据: {blockId: hardness}
_BlockHardnessCache = {}


# endregion


# region 计算相关
def GetRotByPos(startPos, endPos):
    """根据两个位置计算旋转角度"""
    # 计算向量
    vector = commonApiMgr.GetVector(startPos, endPos)
    return serverApi.GetRotFromDir(vector)


# endregion


# region 属性
def IsCreativeMode(playerId):
    """判断是否是创造模式"""
    gameComp = compFactory.CreateGame(levelId)
    mode = gameComp.GetPlayerGameType(playerId)
    return mode == minecraftEnum.GameType.Creative


def GetEntityDimension(entityId):
    """获取实体所在的维度"""
    dimComp = compFactory.CreateDimension(entityId)
    return dimComp.GetEntityDimensionId()


def IsRider(playerId, rideId):
    """判断玩家是否是驾驶员"""
    rideComp = compFactory.CreateRide(rideId)
    riders = rideComp.GetRiders()
    # [{'entityId': '-4294967295', 'seatIndex': 0, 'riderIndex': 0}]
    isRider = False
    # 如果玩家是坐第一个位置，就是驾驶员
    for val in riders:
        if val.get("seatIndex") == 0:
            if val.get("entityId") == playerId:
                isRider = True
            break
    return isRider


def GetAllRiders(entityId):
    """获取实体的所有乘客"""
    rideComp = compFactory.CreateRide(entityId)
    riders = rideComp.GetRiders()
    riderList = []
    for val in riders:
        riderId = val.get("entityId")
        if riderId:
            riderList.append(riderId)
    return riderList


# endregion


# region 实体相关
def SpawnEntity(serverSystem, engineTypeStr, pos, rot=(0, 0), dimension=0, isNpc=False):
    """根据engineTypeStr生成实体，如果生成位置不对，自行调整pos"""
    entityId = serverSystem.CreateEngineEntityByTypeStr(engineTypeStr, pos, rot, dimension, isNpc)
    return entityId


def SpawnEntityById(serverSystem, entityId, engineTypeStr, offset=(0, 0, 0), rot=None, isNpc=False):
    """根据engineTypeStr，在entityId附近生成实体"""
    posComp = compFactory.CreatePos(entityId)
    pos = posComp.GetFootPos()
    if pos:
        dimensionComp = compFactory.CreateDimension(entityId)
        dimension = dimensionComp.GetEntityDimensionId()
        if rot is None:
            rotComp = compFactory.CreateRot(entityId)
            rot = rotComp.GetRot()
        # 如果实体有“is_stackable”组件，会被该位置的实体挤开，从而表现上会是生成位置和pos对不上
        setPos = (pos[0] + offset[0], pos[1] + offset[1], pos[2] + offset[2])
        entityId = serverSystem.CreateEngineEntityByTypeStr(engineTypeStr, setPos, rot, dimension, isNpc)
        return entityId
    return None


def SpawnProjectile(srcId, engineTypeStr, pos, rot, damage=None, power=None, gravity=None):
    """
    根据engineTypeStr，创建抛射物
    :param srcId 发射抛射物的实体id
    :param rot=(pitch, yaw) 抛射物的发射角度
    """
    param = {
        "position": pos,
        "direction": serverApi.GetDirFromRot(rot),
    }
    # 这些有传递才设置；不传递参数将采用行为包中的配置值
    if damage:
        param["damage"] = damage
    if power:
        param["power"] = power
    if gravity:
        param["gravity"] = gravity
    projectileComp = compFactory.CreateProjectile(levelId)
    projectileId = projectileComp.CreateProjectileEntity(srcId, engineTypeStr, param)
    return projectileId


def GetNearbyPlayerList(dimension, centerPos, radius):
    """获取附近玩家列表"""
    playerList = []
    radiusSqrt = radius * radius
    for playerId in serverApi.GetPlayerList():
        dim = GetEntityDimension(playerId)
        if dim == dimension:
            posComp = compFactory.CreatePos(playerId)
            pos = posComp.GetFootPos()
            if commonApiMgr.GetDistanceXZSqrt(centerPos, pos) <= radiusSqrt:
                playerList.append(playerId)
    return playerList


def GetPlayerListByDimension(dimension):
    """获取指定维度的玩家列表"""
    playerList = []
    for playerId in serverApi.GetPlayerList():
        dim = GetEntityDimension(playerId)
        if dim == dimension:
            playerList.append(playerId)
    return playerList


# endregion


# region 物品相关
def GetPlayerItem(playerId, posType, slot):
    """获取玩家身上的物品"""
    itemComp = compFactory.CreateItem(playerId)
    item = itemComp.GetPlayerItem(posType, slot, True)
    return item


def GetPlayerInventoryItemList(playerId):
    """获取玩家背包物品，返回list"""
    # 获取玩家的背包物品
    itemListDict = GetInventoryItems(playerId)
    return itemListDict


def GetPlayerInventoryItems(playerId):
    """获取玩家背包物品，返回dict"""
    # 获取玩家的背包物品
    itemListDict = GetInventoryItems(playerId)
    # 改成slot格式
    itemDict = {}
    slot = 0
    for item in itemListDict:
        if item:
            itemDict[slot] = item
        slot += 1
    return itemDict


def GetInventoryItems(playerId):
    """获取玩家背包的所有物品数据，返回list"""
    itemComp = compFactory.CreateItem(playerId)
    # 格式：[ {item}, None, {item} ]
    itemListDict = itemComp.GetPlayerAllItems(minecraftEnum.ItemPosType.INVENTORY, True)
    return itemListDict


def UpdateCarriedItemDurability(entityId, durability, itemName, aux=None):
    """更新实体手持物品的耐久，如果物品不对，则无法扣除
    :param durability 更新的耐久，负数表示扣耐久
    """
    itemComp = compFactory.CreateItem(entityId)
    # 判断物品是否一致
    item = itemComp.GetPlayerItem(minecraftEnum.ItemPosType.CARRIED, 0)
    if item and item.get("newItemName") == itemName:
        if aux is None or item.get("newAuxValue") == aux:
            hasDurability = item.get("durability", 0) + durability
            if hasDurability <= 0:
                # 清除物品
                itemComp.SpawnItemToPlayerCarried({"newItemName": "minecraft:air", "newAuxValue": 0, "count": 0},
                                                  entityId)
            else:
                itemComp.SetItemDurability(minecraftEnum.ItemPosType.CARRIED, 0, item.get("durability", 0) + durability)
    pass


def DeductItemCount(playerId, itemName, deductCount, posType, slot=0):
    """扣除物品数量，如果物品不对 or 数量不足，则不能扣除"""
    itemComp = compFactory.CreateItem(playerId)
    item = itemComp.GetPlayerItem(posType, slot)
    # id、数量校验
    if item and item.get("newItemName") == itemName and item.get("count", 0) >= deductCount:
        count = item.get("count", 0)
        hasCount = count - deductCount
        # 如果是手持槽位，则获取slot
        if posType == minecraftEnum.ItemPosType.CARRIED:
            slot = itemComp.GetSelectSlotId()
        itemComp.SetInvItemNum(slot, hasCount)
        return True
    return False


def DeductMultiItemsCount(playerId, materialsList):
    """
    扣除多个物品的数量，如果物品数量不足，则不能扣除
    
    materialsList 物品列表，格式：[ {newItemName, newAuxValue, count}, ... ]，aux不设置表示任意aux都可以使用
    """
    itemDictList = GetPlayerInventoryItemList(playerId)
    slotItemDict = {}

    # 先校验数量是否足够
    hasEnough = True
    for item in materialsList:
        itemName = item.get("newItemName")
        aux = item.get("newAuxValue")
        needCount = item.get("count", 0)
        if needCount <= 0:
            continue
        key = itemName
        if aux is not None:
            key = (itemName, aux)
        slotItemDict[key] = {}
        for slot, invItem in enumerate(itemDictList):
            if invItem and invItem.get("newItemName") == itemName:
                if aux is None or invItem.get("newAuxValue") == aux:
                    if invItem.get("count", 0) > 0:
                        needCount -= invItem["count"]
                        slotItemDict[key][slot] = invItem["count"]
                        if needCount <= 0:
                            # 数量足够
                            break
        if needCount > 0:
            # 数量不足
            hasEnough = False
            break
    if hasEnough:
        # 扣除物品
        itemComp = compFactory.CreateItem(playerId)
        for item in materialsList:
            itemName = item.get("newItemName")
            aux = item.get("newAuxValue")
            needCount = item.get("count", 0)
            if needCount <= 0:
                continue
            key = itemName
            if aux is not None:
                key = (itemName, aux)
            if slotItemDict.get(key):
                for slot, count in slotItemDict[key].iteritems():
                    # 扣除指定数量
                    if needCount >= count:
                        itemComp.SetInvItemNum(slot, 0)
                        needCount -= count
                    else:
                        itemComp.SetInvItemNum(slot, count - needCount)
                        needCount = 0
                    if needCount <= 0:
                        # 扣完
                        break
        return True
    return False


def GetItemMaxStackSize(itemName, aux):
    """获取物品堆叠上限"""
    return itemApi.GetItemMaxStackSize(compFactory, levelId, itemName, aux)


def IsCanStack(item1, item2):
    """判断两个物品是否可堆叠，判断userData、extraId、customTips、堆叠上限、"""
    if item1 is None or item2 is None:
        return False
    # 获取堆叠
    stackSize = GetItemMaxStackSize(item1.get("newItemName"), item1.get("newAuxValue"))
    return itemApi.IsCanStack(item1, item2, stackSize)


def SpawnItemsToInventory(serverHandler, playerId, itemList):
    """
    将多个物品放入玩家背包，多余的物品生成在世界中
    每个物品的数量可以设置超过堆叠数
    """
    itemComp = compFactory.CreateItem(playerId)
    # 背包所有物品
    inventoryItemList = GetInventoryItems(playerId)
    changeItems = {}
    invEnum = minecraftEnum.ItemPosType.INVENTORY
    # 遍历生成物品
    i = 0
    lens = len(itemList)
    while i < lens:
        item = itemList[i]
        if item is None:
            i += 1
            continue
        # 格式化处理: 数量必须要有
        if item.get("count") is None:
            item["count"] = 1
        # 格式化item信息
        itemApi.FormatItemInfo(item)

        # 遍历玩家背包物品
        for slot in xrange(0, 36):
            sitem = inventoryItemList[slot]
            if IsCanStack(sitem, item):
                # 可堆叠，按照数量进行堆叠
                stack = GetItemMaxStackSize(item.get("newItemName"), item.get("newAuxValue", 0))
                # 总数
                totalCount = sitem.get("count", 0) + item.get("count", 0)
                if totalCount <= stack:
                    sitem["count"] = totalCount
                    changeItems[(invEnum, slot)] = sitem
                    item = None
                    break
                elif sitem["count"] < stack:
                    sitem["count"] = stack
                    changeItems[(invEnum, slot)] = sitem
                    # 修改剩余没生成的数量
                    item["count"] = totalCount - stack
            elif sitem is None or sitem.get("newItemName") == "minecraft:air":
                # 空格子，直接放入（需判断堆叠上限）
                stack = GetItemMaxStackSize(item.get("newItemName"), item.get("newAuxValue", 0))
                setItem = item
                if item.get("count") > stack:
                    # 该物品超过堆叠上限，则放入堆叠上限的数量，剩余的继续遍历
                    setItem = commonApiMgr.DeepCopy(item)
                    setItem["count"] = stack
                    item["count"] = item["count"] - stack
                    changeItems[(invEnum, slot)] = setItem
                    # 更新背包缓存
                    inventoryItemList[slot] = setItem
                else:
                    # 全部放入
                    changeItems[(invEnum, slot)] = item
                    # 更新背包缓存
                    inventoryItemList[slot] = item
                    item = None
                    break
        if item is None:
            # 该物品已生成完成
            itemList[i] = None
        # 没生成完的，也即没有空格子了，则数据仍存储在list中，等后面生成到世界
        i += 1

    # 将物品生成到玩家背包
    itemComp.SetPlayerAllItems(changeItems)

    # 将物品生成到世界中
    for item in itemList:
        if item:
            SpawnItemToWorld(serverHandler, playerId, item)

    # 记录更新物品数据
    updateItemDict = {}
    for key, item in changeItems.iteritems():
        updateItemDict[key[1]] = item
    return updateItemDict


def SpawnItemToWorld(serverHandler, entityId, item, pos=None, dimension=None):
    """将物品生成到世界中"""
    if not pos:
        posComp = compFactory.CreatePos(entityId)
        pos = posComp.GetFootPos()
        # 高度往上偏移一点，以免卡到地底
        pos = (pos[0], pos[1] + 1, pos[2])
    if dimension is None:  # 不能用not，dim有可能是0
        dimComp = compFactory.CreateDimension(entityId)
        dimension = dimComp.GetEntityDimensionId()
    itemEntityId = serverHandler.CreateEngineItemEntity(item, dimension, pos)
    return itemEntityId


def GetItemMaxDurability(itemName):
    """获取物品的最大耐久"""
    return itemApi.GetItemMaxDurability(compFactory, levelId, itemName)


def GetPunishmentExpLevel(item):
    """获取物品的惩罚经验等级"""
    return itemApi.GetPunishmentExpLevel(compFactory, levelId, item)


def SetItemCustomNameSuffix(playerId, itemName, customName, slotType=None, slot=0):
    """设置玩家背包物品的自定义名称的后缀"""
    if slotType is None:
        slotType = serverApi.GetMinecraftEnum().ItemPosType.CARRIED
    itemComp = compFactory.CreateItem(playerId)
    item = itemComp.GetPlayerItem(slotType, slot, True)
    if item and item.get("newItemName") == itemName:
        name = itemComp.GetCustomName(item)
        if name == "":
            # 该物品没有经过命名，则获取名字
            basic = itemComp.GetItemBasicInfo(itemName)
            if basic:
                name = basic.get("itemName")
        if name and name.endswith(customName) is False:
            itemComp.SetCustomName(item, "§r§f{}{}§r".format(name, customName))
            return itemComp.SetPlayerAllItems({(slotType, slot): item})
    return False


# endregion


# region 方块
def GetBlockDigInfo(blockName):
    """
    获取自定义方块的挖掘工具类型、挖掘等级等信息（缓存）
    原版方块需读取config
    """
    digInfo = _BlockDigCache.get(blockName)
    digInfo = None
    if digInfo is None:
        itemComp = compFactory.CreateItem(levelId)
        basic = itemComp.GetItemBasicInfo(blockName)
        # { "tierDict": {"digger": 0-4(int), "destroy_special": False, "level": 0, "id_aux": ***} }
        if basic and basic.get("tier"):
            tier = basic["tier"]
            digInfo = {
                "digger": GetDiggerStr(tier.get("digger", 0)),
                "level": tier.get("level", 0),
                "destroy_special": tier.get("destroy_special", False),
            }
            _BlockDigCache[blockName] = digInfo
    return digInfo


_DiggerToInt = {
    0: "shovel",
    1: "pickaxe",
    2: "axe",
}


def GetDiggerStr(diggerInt):
    """获取挖掘工具类型字符串"""
    return _DiggerToInt.get(diggerInt, diggerInt)


def GetBlockHardness(blockName):
    """获取方块的硬度，小于0表示无法挖掘"""
    hardness = _BlockHardnessCache.get(blockName)
    if hardness is None:
        hardness = -1  # 基岩是-1
        blockComp = compFactory.CreateBlockInfo(levelId)
        basicInfo = blockComp.GetBlockBasicInfo(blockName)
        if basicInfo:
            hardness = basicInfo.get("destroyTime", 0)
        _BlockHardnessCache[blockName] = hardness
    return hardness


def GetRayBlockPos(dimension, rayPos, rayRot, rayDistance=16, ignoreBlocks=[]):
    """
    获取射线命中的第一个方块位置
    :param rayRot(Vector3): 射线方向的单位向量，可用getDirFromRot获取
    :param ignoreBlocks: 忽略的方块id列表(不包含aux)
    """
    pos = None
    blockList = serverApi.getEntitiesOrBlockFromRay(dimension, rayPos, rayRot, rayDistance, False,
                                                    minecraftEnum.RayFilterType.OnlyBlocks)
    if blockList:
        for block in blockList:
            if block.get("type") == "Block" and block.get("identifier") not in ignoreBlocks:
                pos = block.get("pos")
                break
    return pos


# endregion


# region 爆炸
def CreateExplosion(sourceId, playerId, pos, radius, fire=True, breaks=True):
    """
    创建爆炸
    :param sourceId: 爆炸伤害源id
    :param createrId: 爆炸创造者id，必须是玩家id
    """
    # 获取地图规则，根据规则设置火焰、破坏方块的状态
    if fire or breaks:
        gameComp = compFactory.CreateGame(levelId)
        rulesDict = gameComp.GetGameRulesInfoServer()
        optionInfo = rulesDict.get("option_info")
        if optionInfo:
            # 如果关闭了火焰蔓延，则不生成火焰
            if optionInfo.get("fire_spreads") is False:
                fire = False
        cheatInfo = rulesDict.get("cheat_info")
        if cheatInfo:
            # 如果关闭了生物破坏，则不破坏方块
            if cheatInfo.get("mob_griefing") is False:
                breaks = False
    # 设置爆炸
    explosionComp = compFactory.CreateExplosion(levelId)
    return explosionComp.CreateExplosion(pos, radius, fire, breaks, sourceId, playerId)


# endregion


# region 配方
def GetItemRecipes(itemName, aux, tag=None):
    """获取物品的合成配方（合成材料）"""
    return commonApiMgr.GetItemRecipes(compFactory, levelId, itemName, aux, tag)


# endregion


# region API封装
def GetExtraData(entityId, key):
    """获取实体的ExtraData"""
    if entityId is None:
        entityId = levelId
    extraComp = compFactory.CreateExtraData(entityId)
    return extraComp.GetExtraData(key)


def SetExtraData(entityId, key, data):
    """设置实体的ExtraData"""
    if entityId is None:
        entityId = levelId
    extraComp = compFactory.CreateExtraData(entityId)
    return extraComp.SetExtraData(key, data)


def GetTopBlockHeight(pos, dimension):
    """获取地表方块的高度"""
    blockComp = compFactory.CreateBlockInfo(levelId)
    return blockComp.GetTopBlockHeight(pos, dimension)
# endregion
