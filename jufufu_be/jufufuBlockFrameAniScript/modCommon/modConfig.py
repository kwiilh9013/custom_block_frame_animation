# -*- coding: utf-8 -*-


ModName = "jufufuUniversalTag"
ModScriptName = "jufufuBlockFrameAniScript"
ModVersion = '0.0.1'
ModNameSpace = "jufufu"


ServerSystemPath = "%s.modServer.system" % ModScriptName
ClientSystemPath = "%s.modClient.system" % ModScriptName


class ServerSystemEnum(object):
	ServerSystem = "ServerSystem"
	SelectServerSystem = "SelectServerSystem"
	StartServerSystem = "StartServerSystem"


class ClientSystemEnum(object):
	ClientSystem = "ClientSystem"
	SelectClientSystem = "SelectClientSystem"
	StartClientSystem = "StartClientSystem"


ServerSystemList = [
	ServerSystemEnum.ServerSystem,
	ServerSystemEnum.SelectServerSystem,
	ServerSystemEnum.StartServerSystem
]

ClientSystemList = [
	ClientSystemEnum.ClientSystem,
	ClientSystemEnum.SelectClientSystem,
	ClientSystemEnum.StartClientSystem
]
