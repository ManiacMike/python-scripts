#! /usr/bin/env python
# -*- coding: utf-8 -*-


import sys, getopt
import pycurl
import time

class Test:
    def __init__(self):
        self.contents = ''
    def body_callback(self,buf):
        self.contents = self.contents + buf

def catchKeyboardInterrupt(fn):
    	def wrapper(*args):
		try:
			return fn(*args)
		except KeyboardInterrupt:
			print '\n[*] 强制退出程序'
	return wrapper

class CurlMonitor:
    c = None
    t = None
    def __init__(self):
        self.c = pycurl.Curl()
        self.t = Test()
    def call(self,url):
        start_time = time.time()
        self.c.setopt(self.c.URL, url)
        self.c.setopt(pycurl.WRITEFUNCTION,self.t.body_callback)
        #c.setopt(c.WRITEFUNCTION, t.body_callback)
        self.c.perform()
        end_time = time.time()
        duration = end_time - start_time
        #print c.getinfo(pycurl.HTTP_CODE), c.getinfo(pycurl.EFFECTIVE_URL)
        print ' %s seconds'%(duration)

    def __del__(self):
        self.c.close()

@catchKeyboardInterrupt
def main():
    inputCount = 1
    url = "http://www.baidu.com"
    #获取目录参数
    if len(sys.argv) == 2:
        inputCount = int(sys.argv[1])
    elif len(sys.argv) > 2:
        inputCount = int(sys.argv[1])
        url = int(sys.argv[2])

    i = 0
    m = CurlMonitor()
    while(i < inputCount):
        m.call(url)
        i += 1


if __name__ == '__main__' :
	main()