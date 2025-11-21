# -*- encoding: utf-8 -*-

from jufufuBlockFrameAniScript.CodeCore.common.log.logMetaClass import LogMetaClass


class CommonManager(object):
	__metaclass__ = LogMetaClass
	
	def __init__(self, system):
		self.mSystem = system