# -*- coding: utf-8 -*-
import math

class Quaternion():
	@staticmethod
	def Euler(x, y, z):
		x, y, z = math.radians(x), math.radians(y), math.radians(z)

		cz = math.cos(z * 0.5)
		sz = math.sin(z * 0.5)
		cx = math.cos(x * 0.5)
		sx = math.sin(x * 0.5)
		cy = math.cos(y * 0.5)
		sy = math.sin(y * 0.5)

		qw = cz * cx * cy + sz * sx * sy
		qx = cz * sx * cy - sz * cx * sy
		qy = cz * cx * sy + sz * sx * cy
		qz = sz * cx * cy - cz * sx * sy

		return qw, qx, qy, qz

	@staticmethod
	def RotateVector(q, v):
		v = (0, v[0], v[1], v[2])
		return tuple(Quaternion.Multiply(Quaternion.Multiply(q, v), Quaternion.Conjugate(q))[1:])

	@staticmethod
	def Multiply(q1, q2):
		w1, x1, y1, z1 = q1
		w2, x2, y2, z2 = q2
		return (
			w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2,
			w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2,
			w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2,
			w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2
		)

	@staticmethod
	def Conjugate(q):
		return q[0], -q[1], -q[2], -q[3]

	@staticmethod
	def ToEuler(q):
		w, x, y, z = q
		t0 = 2 * (w * x + y * z)
		t1 = 1 - 2 * (x * x + y * y)
		roll = math.atan2(t0, t1)

		t2 = 2 * (w * y - z * x)
		t2 = min(max(t2, -1), 1)
		pitch = math.asin(t2)

		t3 = 2 * (w * z + x * y)
		t4 = 1 - 2 * (y * y + z * z)
		yaw = math.atan2(t3, t4)

		return tuple(math.degrees(angle) for angle in (roll, pitch, yaw))

	@staticmethod
	def AxisAngle(axis, angle):
		axis_magnitude = math.sqrt(sum(x * x for x in axis))
		if axis_magnitude != 0:
			axis = tuple(x / axis_magnitude for x in axis)

		angle = math.radians(angle)
		s = math.sin(angle / 2)
		c = math.cos(angle / 2)

		return (
			c,
			s * axis[0],
			s * axis[1],
			s * axis[2]
		)

	@staticmethod
	def LookDirection(direction=(0, 0, 1), up=(0, 1, 0)):
		def normalize(v):
			length = math.sqrt(sum(x * x for x in v))
			return tuple(x / length for x in v) if length != 0 else v

		def negative(v):
			return tuple(-x for x in v)

		def cross_product(a, b):
			return (
				a[1] * b[2] - a[2] * b[1],
				a[2] * b[0] - a[0] * b[2],
				a[0] * b[1] - a[1] * b[0]
			)
		# 规范化输入向量
		forward = negative(normalize(direction))
		up = normalize(up)

		# 计算右向量
		right = normalize(cross_product(forward, up))

		# 重新计算up向量以确保正交性
		up = cross_product(right, forward)

		# 构建旋转矩阵 (列主序)
		m = [
			right[0], up[0], -forward[0], 0,
			right[1], up[1], -forward[1], 0,
			right[2], up[2], -forward[2], 0,
			0, 0, 0, -1
		]

		# 将旋转矩阵转换为四元数
		trace = m[0] + m[5] + m[10]
		if trace > 0:
			s = 0.5 / math.sqrt(trace + 1.0)
			w = 0.25 / s
			x = (m[9] - m[6]) * s
			y = (m[2] - m[8]) * s
			z = (m[4] - m[1]) * s
		else:
			if m[0] > m[5] and m[0] > m[10]:
				s = 2.0 * math.sqrt(1.0 + m[0] - m[5] - m[10])
				w = (m[9] - m[6]) / s
				x = 0.25 * s
				y = (m[1] + m[4]) / s
				z = (m[2] + m[8]) / s
			elif m[5] > m[10]:
				s = 2.0 * math.sqrt(1.0 + m[5] - m[0] - m[10])
				w = (m[2] - m[8]) / s
				x = (m[1] + m[4]) / s
				y = 0.25 * s
				z = (m[6] + m[9]) / s
			else:
				s = 2.0 * math.sqrt(1.0 + m[10] - m[0] - m[5])
				w = (m[4] - m[1]) / s
				x = (m[2] + m[8]) / s
				y = (m[6] + m[9]) / s
				z = 0.25 * s

		return w, x, y, z
	