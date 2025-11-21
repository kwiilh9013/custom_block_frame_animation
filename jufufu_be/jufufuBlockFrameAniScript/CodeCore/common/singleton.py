# -*- coding: utf-8 -*-


class Singleton(object):
	def init(self, *args, **kwargs):
		pass

	def __new__(cls, *args, **kwargs):
		if not hasattr(cls, "_instance"):
			cls._instance = object.__new__(cls)
			cls._instance.init(*args, **kwargs)
		return cls._instance


class SingletonMeta(type):
	def __init__(cls, name, bases, dict):
		super(SingletonMeta, cls).__init__(name, bases, dict)
		cls._instance = None

	def __call__(cls, *args, **kwargs):
		if cls._instance is None:
			cls._instance = super(SingletonMeta, cls).__call__(*args, **kwargs)
		return cls._instance
