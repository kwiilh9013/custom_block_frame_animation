# -*- coding: utf-8 -*-
from jufufuBlockFrameAniScript.modCommon.manager import singleton


class SingletonGac(object):
	__metaclass__ = singleton.Singleton


Instance = SingletonGac()
