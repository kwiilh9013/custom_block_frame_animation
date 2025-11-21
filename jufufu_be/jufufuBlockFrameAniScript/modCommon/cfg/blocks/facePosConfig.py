# -*- coding: utf-8 -*-

_faceCenterPosOffset = {
	0: (0.5, -0.01, 0.5),
	1: (0.5, 1.01, 0.5),
	2: (0.5, 0.5, -0.01),
	3: (0.5, 0.5, 1.01),
	4: (-0.01, 0.5, 0.5),
	5: (1.01, 0.5, 0.5)}

def GetBlockCenterPosOffset(face):
	"""获取中心偏移"""
	return _faceCenterPosOffset.get(face)