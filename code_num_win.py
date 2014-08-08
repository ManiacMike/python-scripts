# coding=gbk
import os

def ask_dir(word):
	input_dirname = raw_input(word+"\n")
	if os.path.isdir(input_dirname) == True:
		print (input_dirname+"内代码总行数："+str(get_line_num(input_dirname)))
	else:
		ask_dir("输入目录有误，请重新输入：")


def get_line_num(dirname):
	listfile=os.listdir(dirname)
	linenum = 0
	for filename in listfile:
		if filename[-4:]=='.php':
			out = open(dirname+'/'+filename,'r')
			for line in out:
				linenum = linenum+1
		elif os.path.isdir(dirname+ '\\'+ filename) == True:
			linenum += get_line_num(dirname+ '\\'+ filename)
			print(dirname+'\\'+ filename)
	return linenum

ask_dir("请输入要统计的目录")
raw_input("\n确定退出")
