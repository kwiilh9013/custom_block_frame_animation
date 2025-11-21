# -*- encoding: utf-8 -*-

"""
客户端、服务端 通用的 物品相关API、功能
"""

# region 变量区
# 物品最大耐久的缓存: {name: 耐久}
_ItemMaxDurabilityCache = {}

# 物品堆叠数缓存
_ItemMaxStackSizeCache = {}

# 工具挖掘数据：工具类型、挖掘等级
_TooDigCache = {}


# endregion


def IsOnceItem(item1, item2):
    """判断两个物品是否是同一种物品，判断id、aux"""
    if not IsEmptyItem(item1) and not IsEmptyItem(item2):
        if item1.get("newItemName") == item2.get("newItemName"):
            if item1.get("newAuxValue") == item2.get("newAuxValue"):
                return True
    return False


def IsEmptyItem(item):
    """判断是否为空物品"""
    return item is None or item.get("newItemName") is None or item.get("newItemName") == "minecraft:air" or item.get(
        "newItemName") == "" or item.get("count", 0) <= 0


def IsCanStack(item1, item2, item1StackSize):
    """判断两个物品是否可堆叠，判断userData、extraId、customTips、堆叠上限、"""
    if IsOnceItem(item1, item2):
        if item1StackSize <= 1:
            # 单物品，不可堆叠
            return False
        # 判断其他数据（userData、extraId、customTips），如果有数据不一样，则无法堆叠（需判断空的情况，传递过来的数据不一定有这些数据）
        if item1.get("userData", None) == item2.get("userData", None):
            if item1.get("extraId", "") == item2.get("extraId", ""):
                if item1.get("customTips", "") == item2.get("customTips", ""):
                    return True
    return False


def GetItemMaxStackSize(compFactory, levelId, itemName, aux):
    """获取物品堆叠上限（缓存）"""
    # 优先获取缓存
    stack = _ItemMaxStackSizeCache.get((itemName, aux))
    if stack:
        return stack
    if aux is None:
        aux = 0
    # 通过API获取
    itemComp = compFactory.CreateItem(levelId)
    basicInfo = itemComp.GetItemBasicInfo(itemName, aux)
    if basicInfo:
        size = basicInfo.get("maxStackSize")
        _ItemMaxStackSizeCache[(itemName, aux)] = size
        return size
    return 1


def GetItemMaxDurability(compFactory, levelId, itemName):
    """获取物品的最大耐久（缓存）"""
    maxDurability = _ItemMaxDurabilityCache.get(itemName)
    if maxDurability is None:
        maxDurability = 0
        itemComp = compFactory.CreateItem(levelId)
        basic = itemComp.GetItemBasicInfo(itemName)
        if basic:
            maxDurability = basic.get("maxDurability", 0)
            _ItemMaxDurabilityCache[itemName] = maxDurability
    return maxDurability


def GetItemDigInfo(compFactory, levelId, itemName):
    """获取物品的工具类型、挖掘等级等信息（缓存）"""
    digInfo = _TooDigCache.get(itemName)
    if digInfo is None:
        itemComp = compFactory.CreateItem(levelId)
        basic = itemComp.GetItemBasicInfo(itemName)
        if basic:
            itemType = basic.get("itemType")
            if itemType:
                # 部分物品如剪刀，获取到的level是-1
                itemTierLevel = max(basic.get("itemTierLevel", 0), 0)
                digInfo = {
                    "itemType": itemType,
                    "itemLevel": itemTierLevel,
                }
                _TooDigCache[itemName] = digInfo
    return digInfo


def FormatItemInfo(itemInfo):
    """格式化item数据，即清除多余的数据"""
    if itemInfo and type(itemInfo) == dict:
        # 清除旧的数据
        itemInfo.pop("itemId", None)
        itemInfo.pop("modId", None)
        itemInfo.pop("modItemId", None)
        # TODO 这里会清除itemName、auxValue，所以item数据必须使用new的版本
        itemInfo.pop("itemName", None)
        itemInfo.pop("auxValue", None)
        # 如果有userData，才清除外面的附魔数据；如果附魔数据存在多份，会在做类似自定义箱子的功能时，重启游戏附魔就会提升一级
        if itemInfo.get("userData"):
            itemInfo.pop("enchantData", None)
            itemInfo.pop("modEnchantData", None)
            itemInfo.pop("customTips", None)
            itemInfo.pop("extraId", None)
    return itemInfo


def IsTwoItemSame(newSlotItem, oldSlotItem, compFactory, levelId):
    # 判定两个槽位的物品是否一样，如果一样，加起来的数量是否小于等于其最大堆叠数量
    if not newSlotItem:
        return True
    itemName1 = newSlotItem.get("newItemName", None)
    itemName2 = oldSlotItem.get("newItemName", None)
    if any([itemName2, itemName1]) is None:
        return False
    if itemName1 != itemName2:
        return False
    userData1 = newSlotItem.get("userData", None)
    userData2 = oldSlotItem.get("userData", None)
    if userData1 != userData2:
        return False
    dur1 = newSlotItem.get("durability", None)
    dur2 = oldSlotItem.get("durability", None)
    if dur1 != dur2: return False
    aux1 = newSlotItem.get("newAuxValue", None)
    aux2 = oldSlotItem.get("newAuxValue", None)
    if aux2 != aux1: return False
    count1 = newSlotItem.get("count", 1)
    count2 = oldSlotItem.get("count", 1)
    maxCount = GetItemMaxStackSize(compFactory, levelId, itemName1, aux1)
    if count2 + count1 > maxCount:
        return False
    return True


def IsSameItem(item1, item2):
    if item1 and item2:
        c1 = item1["count"] + 1
        c2 = item2["count"] + 1
        item1["count"] = 1
        item2["count"] = 1
        isSame = item1 == item2
        item1["count"] = c1 - 1
        item2["count"] = c2 - 1
        return isSame
    return False
# ================ 以下是可能有用的代码逻辑 ===================


def GetPunishmentExpLevel(compFactory, levelId, item):
    """获取物品的惩罚经验等级（用于拆解台拆解物品）"""
    # 铁砧修理规则：每损失25%耐久，修理时会消耗1级经验
    expLv = 0
    # 根据玩家拆解的物品的剩余耐久，决定扣除玩家的经验值
    maxDurability = GetItemMaxDurability(compFactory, levelId, item.get("newItemName"))
    durability = item.get("durability", 0) if item.get("durability", 0) > 0 else 0
    if maxDurability > 0 and durability < maxDurability:
        # 铁砧修理规则：每损失25%耐久，修理时会消耗1级经验
        ratio = item.get("durability", 0) / (maxDurability + 0.0)
        ratio = (1 - ratio) * 100
        expLv = int(ratio // 25 + 1)
    return expLv
