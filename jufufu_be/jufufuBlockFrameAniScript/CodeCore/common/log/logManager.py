# -*- coding: utf-8 -*-
import logging
import time


CRITICAL = logging.CRITICAL
ERROR = logging.ERROR
WARNING = logging.WARN
WARN = logging.WARN
INFO = logging.INFO
DEBUG = logging.DEBUG

STREAM = "stream"
SYSLOG = "syslog"
FILE = "file"
CUSTOM = "custom"


class LogManager(object):
	createdModules = set()
	logLevel = DEBUG
	logHandle = STREAM
	logTag = ''
	sysLogger = None
	customHandler = None


	@staticmethod
	def GetLogger(moduleName):
		if moduleName in LogManager.createdModules:
			return logging.getLogger(moduleName)

		logger = logging.getLogger(moduleName)
		logger.setLevel(LogManager.logLevel)
		logger.propagate = False
		if not logger.handlers:
			logger.addHandler(LogManager._CreateHandler(logger))
		LogManager.createdModules.add(moduleName)

		return logger

	@staticmethod
	def _CreateHandler(logger):
		formatlist = ['[%(asctime)s]', '[%(levelname)s]', '[$%(name)s]', '%(message)s']
		if LogManager.logHandle == SYSLOG:
			pass
		elif LogManager.logHandle == FILE:
			pass
		elif LogManager.logHandle == CUSTOM:
			ch = LogManager.customHandler()
		else:
			ch = logging.StreamHandler()

		ch.setLevel(LogManager.logLevel)
		formatter = logging.Formatter(' '.join(formatlist))
		ch.setFormatter(formatter)

		return ch

	@staticmethod
	def SetLogLevel(lv):
		LogManager.logLevel = lv
		for name in LogManager.createdModules:
			logging.getLogger(name).setLevel(lv)

	@staticmethod
	def SetLogHandle(handle):
		LogManager.logHandle = handle
		for name in LogManager.createdModules:
			logger = logging.getLogger(name)
			logger.handlers = []
			logger.addHandler(LogManager._CreateHandler(logger))

	@staticmethod
	def SetLogTag(logTag):
		LogManager.logTag = logTag
		for name in LogManager.createdModules:
			logger = logging.getLogger(name)
			logger.handlers = []
			logger.addHandler(LogManager._CreateHandler(logger))

	@staticmethod
	def SetCustomHandler(handler):
		LogManager.logHandle = CUSTOM
		LogManager.customHandler = handler
