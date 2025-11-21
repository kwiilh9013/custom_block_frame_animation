# -*- coding: utf-8 -*-
from jufufuBlockFrameAniScript.CodeCore.common.log.logManager import LogManager


class LogMetaClass(type):
	def __new__(cls, name, bases, dct):
		entityClass = super(LogMetaClass, cls).__new__(cls, name, bases, dct)
		entityClass.logger = LogManager.GetLogger(entityClass.__name__)
		return entityClass
