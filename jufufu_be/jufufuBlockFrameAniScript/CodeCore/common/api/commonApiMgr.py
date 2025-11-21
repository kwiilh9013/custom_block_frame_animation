# -*- encoding: utf-8 -*-
import math
from jufufuBlockFrameAniScript.CodeCore.utils.vector import Vector3

"""

服务端、客户端都会用到的逻辑

"""


# region 变量区
# endregion


# region 计算功能
def GetDistanceSqrt(pos1, pos2):
    """计算两个位置的距离平方值，未开方"""
    if pos1 is None or pos2 is None:
        return 2147483647  # 整数最大值，mod不能使用sys库
    return (pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2 + (pos1[2] - pos2[2]) ** 2


def GetDistance(pos1, pos2):
    """计算两个位置的距离"""
    return math.sqrt(GetDistanceSqrt(pos1, pos2))


def GetManhattanDistance(pos1, pos2):
    """计算两个位置的曼哈顿距离"""
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1]) + abs(pos1[2] - pos2[2])


def GetDistanceXZSqrt(pos1, pos2):
    """计算两个位置的xz平面的距离，未开方"""
    if pos1 is None or pos2 is None:
        return 2147483647  # 整数最大值，mod不能使用sys库
    return (pos1[0] - pos2[0]) ** 2 + (pos1[2] - pos2[2]) ** 2


def GetDistanceXZ(pos1, pos2):
    """计算两个位置的xz平面的距离"""
    return math.sqrt(GetDistanceXZSqrt(pos1, pos2))


def GetManhattanDistanceXZ(pos1, pos2):
    """计算两个位置xz平面的曼哈顿距离"""
    return abs(pos1[0] - pos2[0]) + abs(pos1[2] - pos2[2])


def InRectangleRange(centerPos, radius, targetPos):
    """判断一个位置是否在一个矩形范围之内"""
    if abs(centerPos[0] - targetPos[0]) <= radius and abs(centerPos[1] - targetPos[1]) <= radius and abs(
            centerPos[2] - targetPos[2]) <= radius:
        return True
    return False


def GetRotBy180(rot):
    """
    某个角度转换为[-180, 180]
    :param rot: int，某一个角度值
    """
    return (rot + 180) % 360 - 180


def GetRotBy360(rot):
    """
    某个角度转换为[0, 360]
    :param rot: int，某一个角度值
    """
    return rot % 360


def Get90Rot(rot):
    """将角度限制在以90度为一个单位的值，比如 30 -> 0"""
    rot = GetRotBy180(rot)
    if rot < -135 or rot >= 135:
        rot = 180
    elif -135 <= rot < -45:
        rot = -90
    elif -45 <= rot < 45:
        rot = 0
    elif 45 <= rot < 135:
        rot = 90
    return rot


def GetOffsetByRot(rot, length):
    """根据旋转角度和长度计算位置偏移，返回类型为list"""
    offset = [0, 0.0, 0]
    if rot[0] != 0:
        offset[1] = -length * math.sin(math.radians(rot[0]))
        length = abs(length * math.cos(math.radians(rot[0])))
    offset[0] = -length * math.sin(math.radians(rot[1]))
    offset[2] = length * math.cos(math.radians(rot[1]))
    return offset


def GetNextPosByRot(pos, rot, length):
    """根据旋转角度和长度计算下一个位置"""
    offset = GetOffsetByRot(rot, length)
    return pos[0] + offset[0], pos[1] + offset[1], pos[2] + offset[2]


def GetBlockPosByEntityPos(pos):
    """根据实体位置转换为方块位置"""
    # 当pos有负数的情况下，实体坐标取整所得的值，并不是脚底的方块坐标
    blockPos = (
        math.floor(pos[0]),
        math.floor(pos[1]),
        math.floor(pos[2])
    )
    return blockPos


def IsCanSee(startPos, endPos, startRotVector, viewRot):
    """判断是否可以看到目标. viewRot=视野角度的一半，单位度"""
    # 根据entity的rot，和target的pos，判断entity是否可以看到target
    # 计算从A到B的方向向量
    dirtVector = GetVector(startPos, endPos)
    # 将方向向量归一化
    dirtVector = VectorNormalize(dirtVector)
    # 计算两个向量的夹角
    angle = VectorAngle(startRotVector, dirtVector)
    # 判断是否在视野范围内
    return angle <= viewRot


def Clamp(value, minValue, maxValue):
    """限制值在最小值和最大值之间"""
    return max(minValue, min(maxValue, value))


def DeepCopy(sourceData):
    """模拟深拷贝，python自带的深拷贝会卡"""
    if isinstance(sourceData, list):
        copyData = []
        for x in sourceData:
            xt = DeepCopy(x)
            copyData.append(xt)
    elif isinstance(sourceData, tuple):
        copyData = []
        for x in sourceData:
            xt = DeepCopy(x)
            copyData.append(xt)
        copyData = tuple(copyData)
    elif isinstance(sourceData, dict):
        copyData = {}
        for k, v in sourceData.iteritems():
            xt = DeepCopy(v)
            copyData[k] = xt
    elif isinstance(sourceData, set):
        copyData = set()
        for x in sourceData:
            xt = DeepCopy(x)
            copyData.add(xt)
    else:
        copyData = sourceData
    return copyData


# endregion


# region 向量计算
def GetVector(startPos, endPos):
    """计算两个位置之间的向量"""
    return endPos[0] - startPos[0], endPos[1] - startPos[1], endPos[2] - startPos[2]


def Vector3CrossProduct(v1, v2):
    """三维向量叉积"""
    return (
        v1[1] * v2[2] - v2[1] * v1[2],
        v1[2] * v2[0] - v2[2] * v1[0],
        v1[0] * v2[1] - v2[0] * v1[1]
    )


def VectorDotProduct(v1, v2):
    """向量点积"""
    return sum((a * b) for a, b in zip(v1, v2))


def VectorLength(v):
    """向量长度"""
    return math.sqrt(sum(a ** 2 for a in v))


def VectorNormalize(v, length=None):
    """向量单位化"""
    if length is None:
        length = VectorLength(v)
    if length > 0:
        return tuple(a / length for a in v)
    return 0, 0, 0


def VectorLerp(v1, v2, t):
    """向量线性插值"""
    if t <= 0:
        return v1
    if t >= 1:
        return v2
    return tuple((1 - t) * v1_i + t * v2_i for v1_i, v2_i in zip(v1, v2))


def VectorLerpLength(v1, v2, t, length=None):
    """向量线性插值，根据长度计算插值，而非比例"""
    if t <= 0:
        return v1
    v = GetVector(v1, v2)
    if length is None:
        length = VectorLength(v)
    if t >= length:
        return v2
    unitV = VectorNormalize(v)
    return tuple(v1_i + t * v2_i for v1_i, v2_i in zip(v1, unitV))


def PlaneNormalVector3(pos1, pos2, pos3):
    """计算三维平面的法向量"""
    # 计算3个点的两个向量
    v1 = (pos2[0] - pos1[0], pos2[1] - pos1[1], pos2[2] - pos1[2])
    v2 = (pos3[0] - pos1[0], pos3[1] - pos1[1], pos3[2] - pos1[2])
    # 叉积得到法向量
    return VectorNormalize(Vector3CrossProduct(v1, v2))


def VectorAngle(v1, v2, v1Len=None, v2Len=None):
    """向量夹角"""
    if v1Len is None:
        v1Len = VectorLength(v1)
    if v2Len is None:
        v2Len = VectorLength(v2)
    if v1Len == 0 or v2Len == 0:
        cosTheta = 0
    else:
        cosTheta = VectorDotProduct(v1, v2) / (v1Len * v2Len)
    return math.degrees(math.acos(cosTheta))


# endregion


# region buff相关
# 原版buff名字
# 增益buff
_MinecraftBuffNameDict = {
    "speed": "速度",
    "haste": "急迫",
    "strength": "力量",
    "jump_boost": "跳跃提升",
    "regeneration": "生命恢复",
    "resistance": "抗性提升",
    "fire_resistance": "抗火",
    "water_breathing": "水下呼吸",
    "invisibility": "隐身",
    "night_vision": "夜视",
    "health_boost": "生命提升",
    "absorption": "伤害吸收",
    "saturation": "饱和",
    "levitation": "漂浮",
    "conduit_power": "潮涌能量",
    "slow_falling": "缓降",
    "village_hero": "村庄英雄",
}
# 减益buff
_MinecraftDebuffNameDict = {
    "slowness": "缓慢",
    "mining_fatigue": "挖掘疲劳",
    "nausea": "恶心",
    "blindness": "失明",
    "hunger": "饥饿",
    "weakness": "虚弱",
    "poison": "中毒",
    "wither": "凋零",
    "fatal_poison": "中毒(致命)",
    "bad_omen": "不祥之兆",
    "darkness": "黑暗",
}


def GetMinecraftBufftName(effectId):
    """获取原版buff名字"""
    return _MinecraftBuffNameDict.get(effectId)


def GetMinecraftDebufftName(effectId):
    """获取原版debuff名字"""
    return _MinecraftDebuffNameDict.get(effectId)


# buff等级
_RomanDict = {
    1: 'I', 4: 'IV', 5: 'V', 9: 'IX', 10: 'X', 40: 'XL', 50: 'L', 90: 'XC',
    100: 'C', 400: 'CD', 500: 'D', 900: 'CM', 1000: 'M'
}
_RomanCache = {}


def GetRomanStr(num):
    """获取罗马数字"""
    res = _RomanCache.get(num)
    if not res:
        res = ""
        for key in sorted(_RomanDict.keys(), reverse=True):
            while num >= key:
                num -= key
                res += _RomanDict[key]
    return res


def GetEffectText(compFactory, levelId, effectId, level, duration):
    """获取buff显示文字，包括等级、持续时间，减益buff红色"""
    # 通过接口获取自定义buff名字
    gameComp = compFactory.CreateGame(levelId)
    name = gameComp.GetChinese(effectId)
    # name为空、或者name和id一样，表示拿不到名字
    if not name or effectId == name:
        # 通过config获取原版buff名字
        name = GetMinecraftBufftName(effectId)
        if name:
            name = "§a" + name
        else:
            name = GetMinecraftDebufftName(effectId)
            if name:
                name = "§c" + name
    lvStr = GetRomanStr(level + 1) if level > 0 else ""
    text = "{} {} ({})§r\n".format(name, lvStr, FormatSeconds(duration))
    return text


# endregion

# region 格式化显示
def FormatSeconds(seconds):
    """格式化秒数"""
    minutes, seconds = divmod(seconds, 60)
    return "%02d:%02d" % (minutes, seconds)


def FormatNumStr(num, strMinLen=0):
    """
    格式化数字字符串，小数部分保留1位
    :param num: 数字
    :param strMinLen: int 数字字符串的最小长度，不足部分用0补位
    """
    numStr = str(num)
    return "{}{:.1f}".format("0" * (strMinLen - len(str(num))), num)


def FormatPercentumStr(num, decimalLen=0):
    """
    格式化数字字符串
    :param num: float 百分比的小数值，0~1之间
    :param decimalLen: int 小数点后保留的位数
    """
    numStr = "{:.{}f}".format(num, decimalLen)
    return numStr
# endregion
