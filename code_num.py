#!/usr/bin/python
# coding=utf-8
import os
import sys

def ask_dir(word):
	input_dirname = raw_input(word+"\n")
	if os.path.isdir(input_dirname) == True:
		print (input_dirname+"的行数是"+str(get_line_num(input_dirname)))
	else:
		ask_dir("找不到这个目录")


def get_line_num(dirname):
	listfile=os.listdir(dirname)
	linenum = 0
	for filename in listfile:
		if filename[-4:]=='.php':
			out = open(dirname + os.path.sep + filename,'r')
			for line in out:
				linenum = linenum+1
		elif os.path.isdir(dirname+ os.path.sep + filename) == True:
			linenum += get_line_num(dirname+ os.path.sep+ filename)
			print(dirname+ os.path.sep + filename)
	return linenum

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

if sys.stdout.encoding == 'cp936':
	sys.stdout = UnicodeStreamFilter(sys.stdout)

if __name__ == '__main__' :
	ask_dir("请输入目录地址")
	raw_input("\n退出")
