#!/usr/bin/python
# coding=utf-8
import urllib, urllib2
import requests
import json
import time
import subprocess

internal_api = "http://188.166.214.158/pokemon.php"

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

def _get(url, jsonfmt = False):
	request = urllib2.Request(url = url)
	response = urllib2.urlopen(request)
	data = response.read()
	if jsonfmt: return json.loads(data, object_hook=_decode_dict)
	return data

def formatTime(timestamp):
	return time.strftime('%H:%M:%S',time.localtime(timestamp))

def main():
    while(True):
        data = _get(internal_api, True)
        if data["status"] == "success" and len(data["pokemons"]) > 0:
            for pokemon in data["pokemons"]:
                print("找到了 %s,位置%s,%s, 消失时间 %s" % (pokemon['pokemon_name_cn'],pokemon["latitude"],pokemon["longitude"],formatTime(pokemon["disappear_time"]/1000)))
                subprocess.call("say 找到了 %s" % pokemon['pokemon_name_cn'],shell=True)
        else:
            pass
        time.sleep(120)

if __name__ == '__main__':
	main()
