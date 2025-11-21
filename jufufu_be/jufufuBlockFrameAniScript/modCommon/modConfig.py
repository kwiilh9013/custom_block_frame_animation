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


class ClientSystemEnum(object):
	ClientSystem = "ClientSystem"
	SelectClientSystem = "SelectClientSystem"


ServerSystemList = [
	ServerSystemEnum.ServerSystem,
	ServerSystemEnum.SelectServerSystem
]

ClientSystemList = [
	ClientSystemEnum.ClientSystem,
	ClientSystemEnum.SelectClientSystem
]
