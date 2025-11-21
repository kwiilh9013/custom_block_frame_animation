# -*- coding:utf-8 -*-
import mod.server.extraServerApi as serverAPI
import math

compFactory = serverAPI.GetEngineCompFactory()
levelId = serverAPI.GetLevelId()


def SetGravity(entityId, g):
    comp = compFactory.CreateGravity(entityId)
    return comp.SetGravity(g)


def GetLevelGravity():
    comp = compFactory.CreateGame(levelId)
    return comp.GetLevelGravity()


def GetGravity(entityId):
    comp = compFactory.CreateGravity(entityId)
    return comp.GetGravity()


def CalMotionByEndPos(entityId, startPos, endPos, t, g=GetLevelGravity(), f=0.02):
    if GetGravity(entityId):
        g = GetGravity(entityId)
    dx, dy, dz = (endPos[0] - startPos[0], endPos[1] - startPos[1], endPos[2] - startPos[2])
    vx = (f * dx) / (1 - math.pow(1 - f, t))
    vy = ((f * dy) - g * t) / (1 - math.pow(1 - f, t)) + g / f - g
    vz = (f * dz) / (1 - math.pow(1 - f, t))
    ans = (vx, vy, vz)
    return ans


def TriggerCustomEvent(entityId, eventName):
    comp = compFactory.CreateEntityEvent(entityId)
    return comp.TriggerCustomEvent(entityId, eventName)


def SetAttrValue(entityId, attrType, value):
    comp = compFactory.CreateAttr(entityId)
    return comp.SetAttrValue(attrType, value)


def SetAttrMaxValue(entityId, attrType, value):
    comp = compFactory.CreateAttr(entityId)
    return comp.SetAttrMaxValue(attrType, value)


def GetAttrValue(entityId, attrType):
    comp = compFactory.CreateAttr(entityId)
    return comp.GetAttrValue(attrType)


def GetAttrMaxValue(entityId, attrType):
    comp = compFactory.CreateAttr(entityId)
    return comp.GetAttrMaxValue(attrType)


def AddTimer(delay, func, *args, **kwargs):
    comp = compFactory.CreateGame(levelId)
    return comp.AddTimer(delay, func, *args, **kwargs)


def AddRepeatTimer(delay, func, *args, **kwargs):
    comp = compFactory.CreateGame(levelId)
    return comp.AddRepeatedTimer(delay, func, *args, **kwargs)


def CancelTimer(timer):
    comp = compFactory.CreateGame(levelId)
    comp.CancelTimer(timer)


def SetEntityRot(entityId, rot):
    comp = compFactory.CreateRot(entityId)
    return comp.SetRot(rot)


def GetEntityPos(entityId):
    comp = compFactory.CreatePos(entityId)
    return comp.GetPos()


def SetEntityPos(entityId, pos):
    comp = compFactory.CreatePos(entityId)
    return comp.SetPos(pos)


def ChangePlayerDimension(playerId, dimensionId, pos):
    if GetEntityDimensionId(playerId) == dimensionId:
        return SetEntityPos(playerId, pos)
    comp = compFactory.CreateDimension(playerId)
    return comp.ChangePlayerDimension(dimensionId, pos)


def SetPlayerRespawnPos(playerId, pos, dimensionId=0):
    comp = compFactory.CreatePlayer(playerId)
    return comp.SetPlayerRespawnPos(pos, dimensionId)


def GetEntityFootPos(entityId):
    comp = compFactory.CreatePos(entityId)
    return comp.GetFootPos()


def GetEntityRot(entityId):
    comp = compFactory.CreateRot(entityId)
    return comp.GetRot()


def GetDirFromRot(rot):
    return serverAPI.GetDirFromRot(rot)


def GetPlayerList():
    return serverAPI.GetPlayerList()


def CreateProjectileEntity(spawnerId, projectileName, param):
    comp = compFactory.CreateProjectile(levelId)
    return comp.CreateProjectileEntity(spawnerId, projectileName, param)


def GetPlayerAllItems(entityId, posType):
    comp = compFactory.CreateItem(entityId)
    return comp.GetPlayerAllItems(posType)


def GetRotFromDir(direction):
    return serverAPI.GetRotFromDir(direction)


def SetMergeSpawnItemRadius(radius):
    gameComp = compFactory.CreateGame(levelId)
    return gameComp.SetMergeSpawnItemRadius(radius)


def GetEntitiesAround(entityId, radius, filters=None, exceptEntity=False):
    comp = compFactory.CreateGame(entityId)
    if filters is None:
        filters = {
            "any_of": [
                {"test": "is_family", "subject": "other", "operator": "not", "value": "player"},
            ]
        }
    entityIds = comp.GetEntitiesAround(entityId, radius, filters)
    if exceptEntity:
        if entityId in entityIds:
            entityIds.remove(entityId)
    return entityIds


def GetEntitiesAroundWithFilter(entityId, radius, filters, exceptEntity=False):
    comp = compFactory.CreateGame(entityId)
    entityIds = comp.GetEntitiesAround(entityId, radius, filters)
    if exceptEntity:
        if entityId in entityIds:
            entityIds.remove(entityId)
    return entityIds


def SetEntityScale(entityId, scale):
    comp = compFactory.CreateScale(entityId)
    return comp.SetEntityScale(entityId, scale)


def GetEntityScale(entityId):
    comp = compFactory.CreateScale(entityId)
    return comp.GetEntityScale()


def GetEntitySize(entityId):
    comp = compFactory.CreateCollisionBox(entityId)
    return comp.GetSize()


def SetEntitySize(entityId, size):
    comp = compFactory.CreateCollisionBox(entityId)
    return comp.SetSize(size)


def GetWorldTime():
    comp = compFactory.CreateTime(levelId)
    return comp.GetTime()


def GetTopBlockHeight(pos, dimensionId=0):
    comp = compFactory.CreateBlockInfo(levelId)
    return comp.GetTopBlockHeight(pos, dimensionId)


def GetBlock(pos, dimensionId=0):
    comp = compFactory.CreateBlockInfo(levelId)
    return comp.GetBlockNew(pos, dimensionId)


def GetBlockBasicInfo(name):
    comp = compFactory.CreateBlockInfo(levelId)
    return comp.GetBlockBasicInfo(name)


def SetBlockNew(pos, blockDict, oldBlockHandling=0, dimensionId=0):
    comp = compFactory.CreateBlockInfo(levelId)
    return comp.SetBlockNew(pos, blockDict, oldBlockHandling, dimensionId)


def GetBlockName(pos, dimensionId=0):
    blockInfo = GetBlock(pos, dimensionId)
    return blockInfo['name'] if blockInfo else 'minecraft:air'


def GetBlockStates(pos, dimensionId=0):
    comp = compFactory.CreateBlockState(levelId)
    return comp.GetBlockStates(pos, dimensionId)


def GetEntityDimensionId(entityId):
    comp = compFactory.CreateDimension(entityId)
    return comp.GetEntityDimensionId()


def SpawnItemToLevel(itemDict, pos, dimensionId=0):
    comp = compFactory.CreateItem(levelId)
    return comp.SpawnItemToLevel(itemDict, dimensionId, pos)


def SpawnItemToPlayerInv(playerId, itemDict, slotPos=-1):
    comp = compFactory.CreateItem(playerId)
    return comp.SpawnItemToPlayerInv(itemDict, playerId, slotPos)


def SpawnItemToPlayerCarried(playerId, itemDict):
    comp = compFactory.CreateItem(playerId)
    return comp.SpawnItemToPlayerCarried(itemDict, playerId)


def GetEntityItem(entityId, posType, slotPos, getUserData=False):
    comp = compFactory.CreateItem(entityId)
    return comp.GetEntityItem(posType, slotPos)


def SetEntityItem(entityId, posType, itemDict, slotPos):
    comp = compFactory.CreateItem(entityId)
    return comp.SetEntityItem(posType, itemDict, slotPos)


def SetItemDurability(entityId, posType, slotPos, durability):
    comp = compFactory.CreateItem(entityId)
    comp.SetItemDurability(posType, slotPos, durability)


def SetItemMaxDurability(entityId, posType, slotPos, maxDurability, isUserData=False):
    comp = compFactory.CreateItem(entityId)
    comp.SetItemMaxDurability(posType, slotPos, maxDurability, isUserData)


def PlaceStructure(pos, name, dimensionId=-1, rot=0, playerId=None):
    comp = compFactory.CreateGame(levelId)
    if playerId is None:
        return comp.PlaceStructure(None, pos, name, dimensionId, rot)
    else:
        return comp.PlaceStructure(playerId, pos, name)


def GetPlayerItem(playerId, posType, slotPos):
    comp = compFactory.CreateItem(playerId)
    return comp.GetPlayerItem(posType, slotPos)


def GetDroppedItem(entityId, flag=False):
    comp = compFactory.CreateItem(levelId)
    return comp.GetDroppedItem(entityId, flag)


def GetSelectSlotId(playerId):
    comp = compFactory.CreateItem(playerId)
    return comp.GetSelectSlotId()


def SetInvItemNum(playerId, slotPos, num):
    comp = compFactory.CreateItem(playerId)
    return comp.SetInvItemNum(slotPos, num)


def ImmuneDamage(entityId, flag):
    comp = compFactory.CreateHurt(entityId)
    comp.ImmuneDamage(flag)


def EnableKeepInventory(playerId, enable):
    comp = compFactory.CreatePlayer(playerId)
    return comp.EnableKeepInventory(enable)


def GetBlockLightLevel(x, y, z, dimensionId):
    comp = compFactory.CreateBlockInfo(levelId)
    return comp.GetBlockLightLevel((x, y, z), dimensionId)


def SetGameRule(ruleDict):
    comp = compFactory.CreateGame(levelId)
    return comp.SetGameRulesInfoServer(ruleDict)


def GetItemBasicInfo(itemName):
    comp = compFactory.CreateItem(levelId)
    return comp.GetItemBasicInfo(itemName)


def GetIdentifierById(entityId):
    comp = compFactory.CreateEngineType(entityId)
    return comp.GetEngineTypeStr()


def SetBlockControlAi(entityId, isBlock):
    comp = compFactory.CreateControlAi(entityId)
    return comp.SetBlockControlAi(isBlock)


def OpenMobHitBlockDetection(entityId, precision):
    comp = compFactory.CreateGame(levelId)
    return comp.OpenMobHitBlockDetection(entityId, precision)


def CloseMobHitBlockDetection(entityId):
    comp = compFactory.CreateGame(levelId)
    return comp.CloseMobHitBlockDetection(entityId)


def SetNPC(entityId):
    actorComp = compFactory.CreateActorPushable(entityId)
    actorRes = actorComp.SetActorPushable(0)
    hurtComp = compFactory.CreateHurt(entityId)
    hurtRes = hurtComp.ImmuneDamage(True)
    return actorRes and hurtRes


def SetPlayerMovable(playerId, isMovable):
    comp = compFactory.CreatePlayer(playerId)
    comp.SetPlayerMovable(isMovable)


def SetPickUpArea(playerId, area):
    comp = compFactory.CreatePlayer(playerId)
    return comp.SetPickUpArea(area)


def OpenEntityHitMobDetection(entityId):
    comp = compFactory.CreatePlayer(entityId)
    return comp.OpenPlayerHitMobDetection()


def CloseEntityHitMobDetection(entityId):
    comp = compFactory.CreatePlayer(entityId)
    comp.ClosePlayerHitMobDetection()


def SetCommand(command, playerId=None, showOutput=False):
    comp = compFactory.CreateCommand(playerId)
    return comp.SetCommand(command, playerId, showOutput)


def SetJumpPower(entityId, jumpPower):
    comp = compFactory.CreateGravity(entityId)
    return comp.SetJumpPower(jumpPower)


def GetEntitiesInSquareArea(startPos, endPos, dimensionId):
    comp = compFactory.CreateGame(levelId)
    return comp.GetEntitiesInSquareArea(None, startPos, endPos, dimensionId)


def NotifyOneMessage(playerId, msg, color='§f'):
    comp = compFactory.CreateMsg(playerId)
    comp.NotifyOneMessage(playerId, msg, color)


def GetEngineType(entityId):
    comp = compFactory.CreateEngineType(entityId)
    entityType = comp.GetEngineType()
    return entityType


def GetEngineTypeStr(entityId):
    comp = compFactory.CreateEngineType(entityId)
    return comp.GetEngineTypeStr()


def AddEffectToEntity(entityId, effectName, duration, amplifier, showParticles=True):
    comp = compFactory.CreateEffect(entityId)
    return comp.AddEffectToEntity(effectName, duration, amplifier, showParticles)


def HasEffect(entityId, effectName):
    comp = compFactory.CreateEffect(entityId)
    return comp.HasEffect(effectName)


def RemoveEffectFromEntity(entityId, effectName):
    comp = compFactory.CreateEffect(entityId)
    return comp.RemoveEffectFromEntity(effectName)


def GetAllEffects(entityId):
    comp = compFactory.CreateEffect(entityId)
    return comp.GetAllEffects()


def ChangePlayerFlyState(playerId, isFly):
    comp = compFactory.CreateFly(playerId)
    return comp.ChangePlayerFlyState(isFly)


def Hurt(toEid, fromEid, damage, cause, knocked=True, childAttackId=None):
    comp = compFactory.CreateHurt(toEid)
    return comp.Hurt(damage, cause, fromEid, childAttackId, knocked)


def CanSee(frmId, targetId, viewRange=8, onlySolid=True, angleX=180.0, angleY=180.0):
    comp = compFactory.CreateGame(frmId)
    return comp.CanSee(frmId, targetId, viewRange, onlySolid, angleX, angleY)


def CheckBlockToPos(fromPos, toPos, dimensionId):
    comp = compFactory.CreateBlockInfo(levelId)
    return comp.CheckBlockToPos(fromPos, toPos, dimensionId)


def RegisterEntityAOIEvent(dimensionId, name, aabb, ignoreEntities=None, entityType=1):
    comp = compFactory.CreateDimension(levelId)
    return comp.RegisterEntityAOIEvent(dimensionId, name, aabb, ignoreEntities, entityType)


def UnRegisterEntityAOIEvent(dimensionId, name):
    comp = compFactory.CreateDimension(levelId)
    return comp.UnRegisterEntityAOIEvent(dimensionId, name)


def SetAddArea(areaKey, minPos, maxPos, dimensionId=0):
    comp = compFactory.CreateChunkSource(levelId)
    comp.SetAddArea(areaKey, dimensionId, minPos, maxPos)


def SetDefaultGameType(gameType):
    comp = compFactory.CreateGame(levelId)
    return comp.SetDefaultGameType(gameType)


def SetPlayerGameType(playerId, gameType):
    comp = compFactory.CreatePlayer(playerId)
    return comp.SetPlayerGameType(gameType)


def GetBiomeName(pos, dimensionId=0):
    comp = compFactory.CreateBiome(levelId)
    return comp.GetBiomeName(pos, dimensionId)


def SetAttackTarget(entityId, targetId):
    comp = compFactory.CreateAction(entityId)
    return comp.SetAttackTarget(targetId)


def ResetAttackTarget(entityId):
    comp = compFactory.CreateAction(entityId)
    return comp.ResetAttackTarget()


def SetName(entityId, name):
    comp = compFactory.CreateName(entityId)
    comp.SetName(name)


def SetTickingArea(playerId, minPos, maxPos, key):
    command = "/tickingarea add {} {} {} {} {} {} {}".format(minPos[0], minPos[1], minPos[2], maxPos[0], maxPos[1],
                                                             maxPos[2], key)
    comp = compFactory.CreateCommand(levelId)
    return comp.SetCommand(command, playerId, False)


def SetPopupNotice(msg1, msg2, color1="BLUE", color2="WHITE"):
    comp = compFactory.CreateGame(levelId)
    comp.SetPopupNotice(msg1, msg2)


def AddBlockItemListenForUseEvent(blockStr):
    comp = compFactory.CreateBlockUseEventWhiteList(levelId)
    return comp.AddBlockItemListenForUseEvent(blockStr)


def RemoveBlockItemListenForUseEvent(blockStr):
    comp = compFactory.CreateBlockUseEventWhiteList(levelId)
    return comp.RemoveBlockItemListenForUseEvent(blockStr)


def SetDisableDropItem(entityId, isDisable):
    comp = compFactory.CreateGame(entityId)
    return comp.SetDisableDropItem(isDisable)


def SetMobKnockback(entityId, xd, zd, power, height, heightCap):
    comp = compFactory.CreateAction(entityId)
    comp.SetMobKnockback(xd, zd, power, height, heightCap)


def SetCutdownMesg(msg, timeTotal):
    timers = []

    def _cb(timeVal):
        SetPopupNotice("", "{} {}s".format(msg, timeVal))
        if timeVal == 1:
            for timer in timers:
                CancelTimer(timer)

    for i in xrange(0, timeTotal):
        timers.append(AddTimer(i, _cb, timeTotal - i))


def GetEntityName(entityId):
    comp = compFactory.CreateName(entityId)
    return comp.GetName()


def GetChunkMinPos(chunkPos):
    comp = compFactory.CreateChunkSource(levelId)
    return comp.GetChunkMinPos(chunkPos)


def GetChunkMaxPos(chunkPos):
    comp = compFactory.CreateChunkSource(levelId)
    return comp.GetChunkMaxPos(chunkPos)


def SetGameDifficulty(difficulty):
    comp = compFactory.CreateGame(levelId)
    return comp.SetGameDifficulty(difficulty)


def LockDifficulty(isLock):
    comp = compFactory.CreateGame(levelId)
    return comp.LockDifficulty(isLock)


def GetTime():
    comp = compFactory.CreateTime(levelId)
    return comp.GetTime()


def SetTime(time):
    comp = compFactory.CreateTime(levelId)
    return comp.SetTime(time)


def KillEntity(entityId):
    comp = compFactory.CreateGame(levelId)
    return comp.KillEntity(entityId)


def GetChinese(langStr):
    comp = compFactory.CreateGame(levelId)
    return comp.GetChinese(langStr).encode('utf-8')


def GetEntityRider(entityId):
    comp = compFactory.CreateRide(entityId)
    return comp.GetEntityRider()


def StopEntityRiding(entityId):
    comp = compFactory.CreateRide(entityId)
    return comp.StopEntityRiding()


def GetOwnerId(entityId):
    comp = compFactory.CreateTame(entityId)
    return comp.GetOwnerId()


def GetAttackTarget(entityId):
    comp = compFactory.CreateAction(entityId)
    target = comp.GetAttackTarget()
    if target == "-1":
        target = None
    return target


def CheckChunkState(dimension, pos):
    comp = compFactory.CreateChunkSource(levelId)
    return comp.CheckChunkState(dimension, pos)


def IsEntityOnFire(entityId):
    comp = compFactory.CreateAttr(entityId)
    return comp.IsEntityOnFire()


def IsEditorMode():
    return serverAPI.GetSystem(serverAPI.GetEngineNamespace(), 'storyline') is not None


def GetValidYRanges(dim, x, y, z, yRange, emptyHeight):
    blockComp = compFactory.CreateBlock(levelId)
    height = yRange
    offsetY = y - height
    palette = blockComp.GetBlockPaletteBetweenPos(dim, (x, y - height, z), (x, y + height, z), False)
    result = palette.GetLocalPosListOfBlocks("minecraft:air")
    yRanges = []
    yStart, yEnd = None, None
    ySize = emptyHeight
    for point in result:
        yCur = point[1]
        if yStart is None:
            yStart = yCur
            yEnd = yStart
        if yCur - yEnd <= 1:
            yEnd = yCur
        else:
            if yEnd - yStart >= ySize:
                yRanges.append((offsetY + yStart, offsetY + yEnd))
            yStart = yCur
            yEnd = yCur
    if yEnd is not None and yEnd - yStart >= ySize:
        yRanges.append((offsetY + yStart, offsetY + yEnd))
    yTop = GetTopBlockHeight((x, z), dim)
    if yTop is not None:
        yTop = int(yTop) + 1
        yRanges.append((yTop, yTop + ySize))
    return yRanges
