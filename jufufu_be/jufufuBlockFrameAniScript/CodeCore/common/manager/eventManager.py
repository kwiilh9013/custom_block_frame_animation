# -*- encoding: utf-8 -*-


class EventMgr(object):
	def __init__(self, handler=None):
		self.mEventDict = {}

	def RegisterEvent(self, eventId, func):
		if eventId not in self.mEventDict:
			self.mEventDict[eventId] = set()
		self.mEventDict[eventId].add(func)

	def NotifyEvent(self, eventId, *args):
		funcs = self.mEventDict.get(eventId)
		if funcs is None:
			return
		for func in funcs:
			try:
				func(*args)
			except Exception as e:
				import traceback
				from jufufuBlockFrameAniScript.CodeCore.common.log import log
				log.logerror(traceback.format_exc())
		pass
	
	def UnRegisterEvent(self, eventId, func):
		if eventId in self.mEventDict:
			self.mEventDict[eventId].discard(func)
	def ClearOne(self, eventId):
		if eventId in self.mEventDict:
			self.mEventDict[eventId].clear()

	def Destroy(self):
		for eventId, funcSet in self.mEventDict.iteritems():
			self.mEventDict[eventId] = None
		self.mEventDict = {}