# -*- encoding: utf-8 -*-

"""
客户端、服务端 通用的 配方相关API、功能
"""


# region 变量区
# endregion


def SplitEnchantBooks(item):
    """
    对附魔书的附魔进行拆分，每个附魔一本书。
    上限9本书，如果超过9个附魔，则最后一本存放剩下的所有附魔
    """
    # userData中的附魔格式: 'userData': {
    #   'ench': [{'lvl': {'__type__': 2, '__value__': 2}, 'id': {'__type__': 2, '__value__': 9}, 'modEnchant': {'__type__': 8, '__value__': ''}}, 
    #       {'lvl': {'__type__': 2, '__value__': 1}, 'id': {'__type__': 2, '__value__': 255}, 'modEnchant': {'__type__': 8, '__value__': 'demoenchant:customenchant4'}}]}, 
    # itemInfo中的附魔格式：'enchantData': [(9, 2)], 'modEnchantData': [('demoenchant:customenchant4', 1)]

    maxCount = 9
    # 存放拆出的附魔书
    itemList = []
    bookId = "minecraft:enchanted_book"
    # 如果有附魔，才进行拆解
    if item.get("userData") and len(item["userData"].get("ench")) > 0:
        # userData中的附魔
        slot = 0
        for i in xrange(len(item["userData"]["ench"])):
            ench = item["userData"]["ench"][i]
            # 根据附魔数量，挨个拆分成单附魔的附魔书；如果有多，则最后一个是存储剩下所有附魔
            if slot == maxCount - 1:
                # 剩下所有附魔，都加到这本书里
                enchItem = {
                    "newItemName": bookId,
                    "newAuxValue": 0,
                    "count": 1,
                    "userData": {
                        "ench": item["userData"]["ench"][i:]
                    }
                }
                itemList.append(enchItem)
                slot += 1
                break
            else:
                # 单个附魔
                enchItem = {
                    "newItemName": bookId,
                    "newAuxValue": 0,
                    "count": 1,
                    "userData": {
                        "ench": [ench]
                    }
                }
                itemList.append(enchItem)
            slot += 1
    elif len(item.get("enchantData")) > 0 or len(item.get("modEnchantData")) > 0:
        # itemInfo中的附魔
        # 根据附魔数量，挨个拆分成单附魔的附魔书；如果有多，则最后一个是存储剩下所有附魔
        slot = 0
        # 原版附魔
        enchCount = len(item.get("enchantData"))
        for i in xrange(enchCount):
            ench = item["enchantData"][i]
            if slot == maxCount - 1:
                # 剩下所有附魔，都加到这本书里
                enchItem = {
                    "newItemName": bookId,
                    "newAuxValue": 0,
                    "count": 1,
                    "enchantData": item["enchantData"][i:],
                }
                itemList.append(enchItem)
                slot += 1
                break
            else:
                enchItem = {
                    "newItemName": bookId,
                    "newAuxValue": 0,
                    "count": 1,
                    "enchantData": [ench],
                }
                itemList.append(enchItem)
            slot += 1
        # 自定义附魔
        enchCount = len(item.get("modEnchantData"))
        for i in xrange(slot, enchCount):
            ench = item["modEnchantData"][i]
            if slot == maxCount - 1:
                # 剩下所有附魔，都加到这本书里
                enchItem = {
                    "newItemName": bookId,
                    "newAuxValue": 0,
                    "count": 1,
                    "modEnchantData": item["modEnchantData"][i:],
                }
                itemList.append(enchItem)
                slot += 1
                break
            else:
                enchItem = {
                    "newItemName": bookId,
                    "newAuxValue": 0,
                    "count": 1,
                    "modEnchantData": [ench],
                }
                itemList.append(enchItem)
            slot += 1
    return itemList


def GetResultCount(recipe, itemName, aux=0):
    """获取配方合成的物品的数量"""
    resultCount = 1
    results = recipe.get("result")
    if type(results) == list:
        # 遍历所有返回物品
        for sresult in results:
            if sresult.get("item") == itemName and sresult.get("data", 0) == aux:
                resultCount = sresult.get("count", 1)
                break
    else:
        resultCount = results.get("count", 1)
    return resultCount


def GetItemRecipes(compFactory, levelId, itemName, aux=0, tag=None):
    """获取配方合成的物品"""
    # 格式
    # {   'pattern': [' A ', 'ABA', 'CCC'],
    #     'result': [{'item': 'minecraft:campfire', 'data': 0 }],
    #     'key': {
    #         'A': { 'item': 'minecraft:stick' },
    #         'C': { 'item': 'minecraft:log2' },
    #         'B': { 'item': 'minecraft:charcoal' }
    # }}
    if tag is None:
        # 默认工作台配方
        tag = "crafting_table"
    recipeComp = compFactory.CreateRecipe(levelId)
    recipesList = recipeComp.GetRecipesByResult(itemName, tag, aux)
    # 做一下针对aux的处理，如果获取不到配方，则用aux=0再获取一遍: 有些情况下，获取的方块aux是非0，就会导致获取不到配方
    if aux > 0 and (recipesList is False or len(recipesList) <= 0):
        recipesList = recipeComp.GetRecipesByResult(itemName, tag, 0)
    if recipesList is False:
        # 因参数数据错误，会返回False，而不是[]
        recipesList = []
    # TODO: 针对微软1.20做适配: 其中某些配方，返回的item中，可能是list，而非str，在list里包含该方块的所有变种id；比如木板(新版本中，木板是不同的id了)
    if tag == "crafting_table":
        lens = len(recipesList)
        for i in xrange(0, lens):
            recipe = recipesList[i]
            # 查看是否有item是list
            if recipe.get("ingredients"):
                # 无序配方
                for item in recipe["ingredients"]:
                    if type(item.get("item")) == list:
                        # 暂时处理：取第一个
                        item["item"] = item["item"][0]
            elif recipe.get("key"):
                # 有序配方
                for item in recipe["key"].values():
                    if type(item.get("item")) == list:
                        # 暂时处理：取第一个
                        item["item"] = item["item"][0]
        pass
    return recipesList
