# -*- encoding: utf-8 -*-
import functools
import inspect


def EngineEvent(priority=0, registerByDefault=True):
	# 直接注册引擎事件，支持有参或者无参事件
	def decorator(func):
		@functools.wraps(func)
		def wrapper(*args, **kwargs):
			#print "[event]:", func.__name__, kwargs
			return func(*args, **kwargs)
		wrapper.eventName = func.__name__
		wrapper.priority = priority
		wrapper.registerByDefault = registerByDefault # 用于动态注册
		return wrapper
	
	return decorator


def AddonEvent(namespace, systemName):
	# 直接注册脚本事件，支持有参或者无参事件
	def decorator(func):
		@functools.wraps(func)
		def wrapper(*args, **kwargs):
			return func(*args, **kwargs)
		wrapper.spaceName = namespace
		wrapper.systemName = systemName
		wrapper.eventName = func.__name__
		wrapper.priority = 0
		wrapper.registerByDefault = True
		return wrapper
	
	return decorator


def ListenEvent(system, instance, namespace, systemName):
	for _, func in inspect.getmembers(instance, inspect.ismethod):
		eventName = getattr(func, "eventName", None)
		if eventName is not None:
			if eventName in instance.__func_list__:
				print "[ERROR]skip duplicate register event with name:", eventName
				continue
			instance.__func_list__.add(eventName)
			registerByDefault = getattr(func, "registerByDefault", False)
			if not registerByDefault:
				continue
			space = getattr(func, "spaceName", None)
			if space:
				realNameSpace = space
			else:
				realNameSpace = namespace
			innerSystemName = getattr(func, "systemName", None)
			if innerSystemName:
				realSystemName = innerSystemName
			else:
				realSystemName = systemName
			system.ListenForEvent(realNameSpace, realSystemName, eventName, instance, func, func.priority)
			# update register flag
			instance.__register_func_list__.add(eventName)


def UnListenEvent(system, instance, namespace, systemName):
	for _, func in inspect.getmembers(instance, inspect.ismethod):
		eventName = getattr(func, "eventName", None)
		if eventName is not None:
			space = getattr(func, "spaceName", None)
			if space:
				realNameSpace = space
			else:
				realNameSpace = namespace
			innerSystemName = getattr(func, "systemName", None)
			if innerSystemName:
				realSystemName = innerSystemName
			else:
				realSystemName = systemName
			system.UnListenForEvent(realNameSpace, realSystemName, eventName, instance, func, func.priority)
			# update register flag
			instance.__register_func_list__.discard(eventName)
