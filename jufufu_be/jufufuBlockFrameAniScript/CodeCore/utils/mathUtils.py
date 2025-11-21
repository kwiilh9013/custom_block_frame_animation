# -*- encoding: utf-8 -*-
import math

from common.utils.mcmath import Quaternion as Quat
from common.utils.mcmath import Vector3 as Vec3
from math import floor


class MathUtils(object):
    @staticmethod
    def Clamp(value, minValue, maxValue):
        # type: (float, float, float) -> float
        return min(max(value, minValue), maxValue)

    @staticmethod
    def Lerp(start, end, t):
        # type: (float, float, float) -> float
        return start + (end - start) * t

    @staticmethod
    def TupleAdd(v1, v2):
        # type: (Tuple[float,...], Tuple[float,...]) -> Tuple[float,...]
        return tuple((a + b) for a, b in zip(v1, v2))

    @staticmethod
    def TupleMin(v1, v2):
        # type: (Tuple[float,...], Tuple[float,...]) -> Tuple[float,...]
        return tuple(min(a, b) for a, b in zip(v1, v2))

    @staticmethod
    def TupleMax(v1, v2):
        # type: (Tuple[float,...], Tuple[float,...]) -> Tuple[float,...]
        return tuple(max(a, b) for a, b in zip(v1, v2))

    @staticmethod
    def TupleSub(v1, v2):
        # type: (Tuple[float,...], Tuple[float,...]) -> Tuple[float,...]
        return tuple((a - b) for a, b in zip(v1, v2))

    @staticmethod
    def TupleAddMul(v1, v2, k):
        # type: (Tuple[float,...], Tuple[float,...], float) -> Tuple[float,...]
        return tuple((a + b * k) for a, b in zip(v1, v2))

    @staticmethod
    def TupleMul(v, k):
        # type: (Tuple[float,...], float) -> Tuple[float,...]
        return tuple((a * k) for a in v)

    @staticmethod
    def TupleLength(v, sqrt=True):
        # type: (Tuple[float,...], float) -> float
        length = 0
        for a in v:
            length += a * a
        if not sqrt:
            return length
        return math.sqrt(length)

    @staticmethod
    def TupleFloor2Int(v):
        # type: (Tuple[float,float,float]) -> Tuple[int,int,int]
        return tuple(map(int, map(floor, v)))

    @staticmethod
    def TupleRound(v, p):
        # type: (Tuple[float,float,float]) -> Tuple[int,int,int]
        return tuple(round(a, p) for a in v)

    @staticmethod
    def LookDirection(direction=Vec3.Forward(), up=Vec3.Up()):
        # type: (Vector3, Vector3) -> Quaternion
        return Quat.LookDirection(-direction, up)

    @staticmethod
    def InverseRot(rot):
        return Quat.Inverse(rot)

    @staticmethod
    def RotByFace(pos, rot):
        ret = pos
        if rot < 0:
            rot += 360
        if rot == 90:
            ret = (-pos[2], pos[1], pos[0])
        elif rot == 180:
            ret = (-pos[0], pos[1], -pos[2])
        elif rot == 270:
            ret = (pos[2], pos[1], -pos[0])
        return ret

    @staticmethod
    def _CubicSplineLerp(points, i, t):
        n = len(points) - 1
        p0 = points[max(i - 1, 0)]
        p1 = points[i]
        p2 = points[min(i + 1, n)]
        p3 = points[min(i + 2, n)]

        t2 = t * t
        t3 = t2 * t

        a = (0.5 * (p2[0] - p0[0]), 0.5 * (p2[1] - p0[1]), 0.5 * (p2[2] - p0[2]))
        b = (0.5 * (p3[1] - p1[1]), 0.5 * (p3[1] - p1[1]), 0.5 * (p3[2] - p1[2]))

        result = [
            (2 * t3 - 3 * t2 + 1) * p1[j] +
            (t3 - 2 * t2 + t) * a[j] +
            (-2 * t3 + 3 * t2) * p2[j] +
            (t3 - t2) * b[j]
            for j in range(3)
        ]
        return tuple(result)

    @staticmethod
    def CubicSplineInterpolation(points, p, total=0.0, splinesDis=None):
        n = len(points) - 1
        t = p * n
        i = int(t)
        t = t - i
        if total > 0 and splinesDis is not None:
            i = 0
            targetDis = p * total
            curDis = 0.0
            t = 0.0
            while i < len(splinesDis):
                temp = curDis + splinesDis[i]
                if temp > targetDis:
                    t = (targetDis - curDis) / splinesDis[i]
                    i -= 1
                    break
                curDis = temp
                i += 1
        if i >= n:
            i = n - 1
            t = 1
        return MathUtils._CubicSplineLerp(points, i, t)

    @staticmethod
    def CubicSplinePrepare(points, disFunc):
        total = 0.0
        splinesDis = [0.0]
        i = 0
        n = len(points) - 1
        while i < n:
            dis = disFunc(points, i, i + 1)
            splinesDis.append(dis)
            total += dis
            i += 1
        return total, splinesDis

    @staticmethod
    def CubicSplineDis(points, ia, ib):
        p0 = points[ia]
        dis = 0.0
        for i in range(0, 20):
            t = float(i + 1.0) / 20.0
            p = MathUtils._CubicSplineLerp(points, ia, t)
            dis += MathUtils.TupleLength(MathUtils.TupleSub(p, p0))
            p0 = p
        return dis

    @staticmethod
    def CubicPosTupleDis(points, ia, ib):
        a = points[ia]
        b = points[ib]
        return MathUtils.TupleLength(MathUtils.TupleSub(a, b))

    @staticmethod
    def CubicRotTupleDis(points, ia, ib):
        a = points[ia]
        b = points[ib]
        q1 = Quaternion.Euler(a[0], a[1], a[2])
        q2 = Quaternion.Euler(b[0], b[1], b[2])
        dot_product = Quaternion.Dot(q1, q2)
        return math.acos(2 * dot_product ** 2 - 1)

    # 根据三维坐标列表，算出相邻坐标的差值，返回一个列表
    @staticmethod
    def GetPointDeltaValue(points=None):
        if not points: return []
        pLen = len(points) - 1
        result = []
        ra = result.append
        for index, a in enumerate(points):
            p0 = a
            p1Index = min(index + 1, pLen)
            p1 = points[p1Index]
            if index + 1 > pLen: continue
            delta = (round(p1[0] - p0[0], 4), round(p1[1] - p0[1], 4), round(p1[2] - p0[2], 4))
            ra(delta)
        return result

    @staticmethod
    def TimeLinearInterpolation(data, num_points_per_unit_time=10):
        # 默认一秒间隔10个点
        interpolated_data = []
        for i in range(len(data) - 1):
            t_start, t_end = data[i][0], data[i + 1][0]
            x_start, x_end = data[i][1], data[i + 1][1]
            y_start, y_end = data[i][2], data[i + 1][2]
            z_start, z_end = data[i][3], data[i + 1][3]
            delta_t = t_end - t_start
            num_points = int(delta_t * num_points_per_unit_time)
            num_points = num_points if num_points != 0 else 1
            for j in range(num_points + 1):
                t_new = t_start + j * delta_t / num_points
                x_new = x_start + j * (x_end - x_start) / num_points
                y_new = y_start + j * (y_end - y_start) / num_points
                z_new = z_start + j * (z_end - z_start) / num_points
                interpolated_data.append((round(t_new, 5), round(x_new, 5), round(y_new, 5), round(z_new, 5)))
        return interpolated_data


class Vector3(Vec3):
    pass


class Quaternion(Quat):
    pass
