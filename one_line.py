#!/usr/bin/python
# coding=utf-8

#一句话python

#画爱心
print('\n'.join([''.join([('Love'[(x-y) % len('Love')] if ((x*0.05)**2+(y*0.1)**2-1)**3-(x*0.05)**2*(y*0.1)**3 <= 0 else ' ') for x in range(-30, 30)]) for y in range(30, -30, -1)]))

#100以内的质数
[n for n in range(1,100) if not [ m for m in range(2,n) if n%m == 0]]

#26个英文字母
[chr(i) for i in range(97,123)]

#9*9乘法表
print ('\n'.join([' '.join(['%s*%s=%-2s' % (y,x,x*y) for y in range(1,x+1)]) for x in range(1,10)]))

#求阶乘
reduce(lambda x, y: x * y, range(1,input(‘number:’)+1), 1)
