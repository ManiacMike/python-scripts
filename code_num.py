#!/usr/bin/python
# coding=utf-8
import os
import sys

def ask_dir(tip):
	input_dirname = raw_input(tip+"\n").strip()
	if os.path.isdir(input_dirname) == True:
		return input_dirname
	else:
		ask_dir("找不到这个目录，重新输入：")


def get_line_num(dirname,fileType):
	listfile=os.listdir(dirname)
	linenum = 0
	for filename in listfile:
		if filename[-4:]=='.'+fileType:
			out = open(dirname + os.path.sep + filename,'r')
			for line in out:
				if line.strip() != "":
					linenum = linenum+1
		elif os.path.isdir(dirname+ os.path.sep + filename) == True:
			linenum += get_line_num(dirname+ os.path.sep+ filename,fileType)
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

def main():
	if sys.stdout.encoding == 'cp936':
		sys.stdout = UnicodeStreamFilter(sys.stdout)
	while True:
		dir = ask_dir("请输入目录地址")
		fileType = raw_input("请输入文件类型\n")
		print (dir+"内 "+fileType+" 代码行数是"+str(get_line_num(dir,fileType)))
		q = raw_input("\nq键退出，任意键继续")
		if q == "q":
			break
	return

if __name__ == '__main__' :
	main()
