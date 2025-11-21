# -*- coding: utf-8 -*-
"""
vector运算
"""
import math


class Vector3:
	"""vector3向量计算"""
	def __init__(self, x=0.0, y=0.0, z=0.0):
		self.x = x
		self.y = y
		self.z = z
	
	def __add__(self, other):
		"""加"""
		return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
	
	def __sub__(self, other):
		"""减"""
		return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)
	
	def __mul__(self, other):
		"""乘"""
		return Vector3(self.x * other, self.y * other, self.z * other)
	
	def __div__(self, other):
		"""除"""
		return Vector3(self.x / other, self.y / other, self.z / other)
	
	def __str__(self):
		"""输出"""
		return "(%f, %f, %f)" % (self.x, self.y, self.z)
	
	def __eq__(self, other):
		"""相等判断"""
		return self.x == other.x and self.y == other.y and self.z == other.z
	
	def __ne__(self, other):
		"""不相等判断"""
		return not self == other
	
	def Length(self):
		"""长度"""
		return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
	
	def Normalize(self):
		"""归一化"""
		length = self.Length()
		if length == 0:
			return Vector3(0, 0, 0)
		return Vector3(self.x / length, self.y / length, self.z / length)
	
	def Lerp(self, other, t):
		"""线性插值"""
		return (other - self) * t + self
	
	def ToTuple(self):
		"""转换为元组"""
		return self.x, self.y, self.z
