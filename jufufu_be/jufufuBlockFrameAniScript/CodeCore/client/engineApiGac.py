# -*- encoding: utf-8 -*-

import mod.client.extraClientApi as clientApi

compFactory = clientApi.GetEngineCompFactory()
levelId = clientApi.GetLevelId()


def AddTimer(delay, func, *args, **kwargs):
	comp = compFactory.CreateGame(levelId)
	return comp.AddTimer(delay, func, *args, **kwargs)


def AddRepeatedTimer(delay, func, *args, **kwargs):
	comp = compFactory.CreateGame(levelId)
	return comp.AddRepeatedTimer(delay, func, *args, **kwargs)


def CancelTimer(timer):
	comp = compFactory.CreateGame(levelId)
	if not comp:
		return False
	return comp.CancelTimer(timer)


def GetEntityPos(entityId):
	comp = compFactory.CreatePos(entityId)
	return comp.GetPos()


def GetEntityFootPos(entityId):
	comp = compFactory.CreatePos(entityId)
	return comp.GetFootPos()


def GetRot(entityId):
	comp = compFactory.CreateRot(entityId)
	return comp.GetRot()


def GetDirFromRot(rot):
	return clientApi.GetDirFromRot(rot)


def SetCanMove(canMove):
	comp = compFactory.CreateOperation(levelId)
	return comp.SetCanMove(canMove)


def SetCanJump(canJump):
	comp = compFactory.CreateOperation(levelId)
	return comp.SetCanJump(canJump)


def SetCanOpenInv(canOpen):
	comp = compFactory.CreateOperation(levelId)
	return comp.SetCanOpenInv(canOpen)


def SetNotRenderAtAll(entityId, notRender):
	if not notRender:
		pass

	comp = compFactory.CreateActorRender(entityId)
	return comp.SetNotRenderAtAll(notRender)


def IsMoving(playerId):
	comp = compFactory.CreatePlayer(playerId)
	return comp.isMoving()


def LockCamera(pos, rot):
	comp = compFactory.CreateCamera(levelId)
	return comp.LockCamera(pos, rot)


def UnLockCamera():
	comp = compFactory.CreateCamera(levelId)
	comp.UnLockCamera()


def CreateTextBoardInWorld(text, textColor, boardColor, faceCamera=True, pos=(0, 0, 0), scale=(1.0, 1.0)):
	comp = compFactory.CreateTextBoard(levelId)
	boardId = comp.CreateTextBoardInWorld(text, textColor, boardColor, faceCamera)
	if boardId:
		comp.SetBoardPos(boardId, pos)
		comp.SetBoardScale(boardId, scale)
	return boardId


def RemoveTextBoard(boardId):
	comp = compFactory.CreateTextBoard(levelId)
	if boardId:
		comp.RemoveTextBoard(boardId)


def SetText(boardId, text):
	comp = compFactory.CreateTextBoard(levelId)
	if boardId:
		comp.SetText(boardId, text)


def GetConfigData(key, isGlobal=False):
	comp = compFactory.CreateConfigClient(levelId)
	return comp.GetConfigData(key, isGlobal)


def SetConfigData(key, data, isGlobal=False):
	comp = compFactory.CreateConfigClient(levelId)
	return comp.SetConfigData(key, data, isGlobal)


def GetLocalPlayerId():
	return clientApi.GetLocalPlayerId()


def SetShowName(entityId, isShow):
	comp = compFactory.CreateName(entityId)
	comp.SetShowName(isShow)


def DoResearch(entityId):
	try:
		comp = compFactory.CreateResearch(entityId)
		comp.ChangeFrequence(0.05)
		comp.SetTime("2022-06-23", "2022-07-24")
		comp.DoShowResearch()
	except Exception as e:
		print "暂未支持调研功能"


def HideNameTag(isHide):
	clientApi.HideNameTag(isHide)


def PlayGlobalCustomMusic(name, volume, loop=True):
	comp = compFactory.CreateCustomAudio(levelId)
	return comp.PlayGlobalCustomMusic(name, volume, loop)


def GetTime():
	comp = compFactory.CreateTime(levelId)
	return comp.GetTime()


def GetChinese(langStr):
	comp = compFactory.CreateGame(levelId)
	return comp.GetChinese(langStr)


def IsDevMode():
	return clientApi.GetSystem(clientApi.GetEngineNamespace(), 'editorConfigCmdSys') is not None


def SetPopupNotice(message, subtitle=""):
	comp = compFactory.CreateGame(levelId)
	return comp.SetPopupNotice(message, subtitle)


def SetTipMessage(msg):
	comp = compFactory.CreateGame(levelId)
	return comp.SetTipMessage(msg)


def HasEntity(entityId):
	comp = compFactory.CreateGame(levelId)
	return comp.HasEntity(entityId)


def IsTamed(entityId):
	queryComp = compFactory.CreateQueryVariable(entityId)
	isTamed = queryComp.GetMolangValue("query.is_tamed")
	return True if isTamed > 0 else False


def GetEngineTypeStr(entityId):
	comp = compFactory.CreateEngineType(entityId)
	return comp.GetEngineTypeStr()


def GetEntitiesAround(entityId, radius, filters={}):
	gameComp = compFactory.CreateGame(entityId)
	return gameComp.GetEntitiesAround(entityId, radius, filters)
