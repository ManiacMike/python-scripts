#!/usr/bin/python
# coding=utf-8

# 阴阳师  还要肝多久才有六星
import math

__author__ = "github/maniacmike"


fiveStarNeed = 5  # 需要5星狗粮5只
whiteDamoNum = 22  # 白达摩数量
threeStarHave = 9  # 已有三星狗粮，注意这不是要升到四星以及以上的
fourStarHave = 1  # 已有四星狗粮，注意这不是要升到五星的
chapter15Exp = 3755  # 2脱4 15章经验加成小怪的经验（0%加成）
# expRate = 1.25 #月卡＋工会
expRate = 1.75  # 月卡＋工会 + 50%加成
battleTime = 35  # 单场需要时间


total = 0
threeStarNeed = 0
level30Exp = 67  # 单个式神30级需要的总经验 单位万
level25Exp = 34  # 单个式神25级需要的总经验
level20Exp = 15  # 单个式神20级需要的总经验

total += fiveStarNeed * level30Exp
fourStarNeed = fiveStarNeed * 4 - fourStarHave
total += fourStarNeed * level25Exp
threeStarNeed = fourStarNeed * 3 - threeStarHave
total += threeStarNeed * level20Exp


if whiteDamoNum <= fiveStarNeed:
    total = total - (level30Exp / 2) * whiteDamoNum
elif whiteDamoNum <= fiveStarNeed * 5:
    total = total - (level30Exp / 2) * fiveStarNeed - \
        (level25Exp / 2) * (whiteDamoNum - fiveStarNeed)
elif whiteDamoNum <= fiveStarNeed * 20:
    total = total - (level30Exp / 2) * fiveStarNeed - (level25Exp / 2) * \
        fiveStarNeed * 4 - (level20Exp / 2) * (whiteDamoNum - fiveStarNeed * 5)
else:
    total = total / 2

print("在当前的设定下，您一共需要：")
print("总共需要经验：" + str(total) + "万exp")
print("需要三星狗粮（升完三星就被吃的）：" + str(threeStarNeed) + "只")

battleNeed = math.ceil(total * 10000 / (chapter15Exp * expRate))
print("总共需要战斗：" + str(battleNeed) + "场")
print("总共需要战斗时间：" + str(battleNeed * battleTime / 3600) + "小时")
