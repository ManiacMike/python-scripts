#!/usr/bin/python
# coding=utf-8

import sys,os,commands
import urllib, urllib2
import cookielib
import requests
import json
# import ssl
import time
# import requests.packages.urllib3.util.ssl_
# requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'


latitudeRange = (37.8089,37.7189)
longitudeRange = (-122.5008,-122.3811)
# longitudeRange = (-122.4687,-122.3811)
step = 0.007
targetPokemon =  {3:'妙蛙花',4:'小火龙',5:'火恐龙',6:'喷火龙',9:'水箭龟',25:'比卡丘',
26:'雷丘',34:'Nidoking',37:'六尾',38:'九尾',40:'胖可丁',58:'卡蒂狗',59:'风速狗',71:'大食花',
76:'石头人',83:'大葱鸭',94:'耿鬼',103:'椰蛋树',105:'嘎拉嘎拉',115:'袋兽',131:'拉普拉斯',
65:'胡地',143:'卡比兽',149:'快龙'}
DEBUG = False
CALLTIMES = 0

#targetPokemon[16] = "波波"


def catchKeyboardInterrupt(fn):
	def wrapper(*args):
		try:
			return fn(*args)
		except KeyboardInterrupt:
			print '\n[*] 强制退出程序'
	return wrapper

class UnicodeStreamFilter:
	def __init__(self, target):
		self.target = target
		self.encoding = 'utf-8'
		self.errors = 'replace'
		self.encode_to = self.target.encoding

	def write(self, s):
		if type(s) == str:
			s = s.decode('utf-8')
		s = s.encode(self.encode_to, self.errors).decode(self.encode_to)
		self.target.write(s)

	def flush(self):
		self.target.flush()

def _decode_list(data):
	rv = []
	for item in data:
		if isinstance(item, unicode):
			item = item.encode('utf-8')
		elif isinstance(item, list):
			item = _decode_list(item)
		elif isinstance(item, dict):
			item = _decode_dict(item)
		rv.append(item)
	return rv

def _decode_dict(data):
	rv = {}
	for key, value in data.iteritems():
		if isinstance(key, unicode):
			key = key.encode('utf-8')
		if isinstance(value, unicode):
			value = value.encode('utf-8')
		elif isinstance(value, list):
			value = _decode_list(value)
		elif isinstance(value, dict):
			value = _decode_dict(value)
		rv[key] = value
	return rv

def _get(url):
	cmd = ''' curl –connect-timeout 3 %s  2>/dev/null ''' % (url)
	result = commands.getoutput(cmd)
	try:
		result = json.loads(result, object_hook=_decode_dict)
		return result
	except:
		return {"status":"fail"}


def getNextPosition(position):
    lat = position[0]
    lon = position[1]
    newLon = lon + step
    if newLon > longitudeRange[1]:#换行
        newLat = lat - step
        if newLat < latitudeRange[1]:
            print("Scan over,restart ",CALLTIMES)
			CALLTIMES = 0
            return (latitudeRange[0],longitudeRange[0]) #返回初始点
        else:
            return (newLat,longitudeRange[0])
    else:
        return (lat,newLon)

def clearExpiriedPokemon(pokemonList):
    for key, pokemon in pokemonList.items():
        if int(time.time()) > pokemon['expiration_time']:
            del pokemonList[key]
        else:
            pass
    return pokemonList

def formatTime(timestamp):
    return time.strftime('%H:%M:%S',time.localtime(timestamp))

@catchKeyboardInterrupt
def main():
    global CALLTIMES
    reload(sys)
    sys.setdefaultencoding('utf8')
    if sys.stdout.encoding == 'cp936':
    	sys.stdout = UnicodeStreamFilter(sys.stdout)
    # opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
    # urllib2.install_opener(opener)

    position = (latitudeRange[0],longitudeRange[0])
    findedPokemon = {}

    while(CALLTIMES < 10000):
        url = "https://pokevision.com/map/data/%s/%s" % (position[0], position[1])
        # print(url)
        data = _get(url)
        if data["status"] == "success" and len(data["pokemon"]) > 0:
            for pokemon in data["pokemon"]:
                ifName = targetPokemon.get(pokemon["pokemonId"])
                if ifName != None and findedPokemon.get(pokemon['id']) == None:#目标pokemon且没有找到过
                    findedPokemon[pokemon['id']] = pokemon
                    print("找到了 %s,位置%s,%s, 消失时间 %s" % (ifName,pokemon["latitude"],pokemon["longitude"],formatTime(pokemon["expiration_time"])))
                else:
                    pass
        else:
            pass
        if DEBUG == True and data["status"] == "success":
            print(position,len(data["pokemon"]))
        findedPokemon = clearExpiriedPokemon(findedPokemon)
        position = getNextPosition(position)
        CALLTIMES += 1


if __name__ == '__main__':
    main()
