# coding=gbk
import os

def ask_dir(word):
	input_dirname = raw_input(word+"\n")
	if os.path.isdir(input_dirname) == True:
		print (input_dirname+"�ڴ�����������"+str(get_line_num(input_dirname)))
	else:
		ask_dir("����Ŀ¼�������������룺")


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

ask_dir("������Ҫͳ�Ƶ�Ŀ¼")
raw_input("\nȷ���˳�")
