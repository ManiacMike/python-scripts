#!/usr/bin/python
# coding=utf-8
import os,shutil
import sys, getopt
import urllib, urllib2
import cookielib
import requests
import subprocess
from HTMLParser import HTMLParser

AV_WEBSITE = "https://avmo.pw"
DUMP_DIR = "/Users/Mike/Downloads/_tmp"

class SearchHtmlParser(HTMLParser):
    def __init__(self):
        self.processing = False
        self.detailUrl = ""
        HTMLParser.__init__(self)
    def handle_starttag(self, tag, attrs):
        if tag == "a" and attrs[0][1] == "movie-box":
            self.detailUrl = attrs[1][1]
            return

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        pass

class DetailHtmlParser(HTMLParser):
    def __init__(self):
        self.imgSrc = ""
        self.prossesingActor = False
        self.actors = []
        HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        if tag == "a" and attrs[0][1] == "bigImage":
            self.imgSrc = attrs[1][1]
        elif tag == "span" and len(attrs) == 0:
            self.prossesingActor = True
        else:
            self.prossesingActor = False

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        if self.prossesingActor == True:
            self.actors.append(data)
            self.prossesingActor = False


def getCoverUrlById(mid):
    searchUrl = AV_WEBSITE + '/cn/search/' + mid
    # print(searchUrl+"\n")
    searchHtmlParser = SearchHtmlParser()
    html = _get(searchUrl)
    searchHtmlParser.feed(html)
    detailUrl = searchHtmlParser.detailUrl
    if detailUrl != "":
        detailHtmlParser = DetailHtmlParser()
        html = _get(detailUrl)
        detailHtmlParser.feed(html)
        return (detailHtmlParser.imgSrc,detailHtmlParser.actors)
    else:
        return ("",[])

def _get(url):
	request = urllib2.Request(url = url)
	response = urllib2.urlopen(request)
	data = response.read()
	return data

def _getFileNameAndExt(filename):
	(filepath,tempfilename) = os.path.split(filename);
	(shotname,extension) = os.path.splitext(tempfilename);
	return shotname,extension

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

def _getMovieId(name):
    if name.find(" ") != -1:
        a = name.split(" ")
    else:
        a = [name,""]
    return a

def _downloadImg(src,filename):
    print(src)
    print(filename)
    subprocess.call("image_downloader -f=\"" + filename + "\" -u=\""+src+"\"",shell=True)
    # data = urllib.urlopen(src).read()
    # f = file(filename,"wb")
    # f.write(data)
    # f.close()

@catchKeyboardInterrupt
def main():
    reload(sys)
    sys.setdefaultencoding('utf8')
    if sys.stdout.encoding == 'cp936':
    	sys.stdout = UnicodeStreamFilter(sys.stdout)

    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
    urllib2.install_opener(opener)

    #获取目录参数
    opts, args = getopt.getopt(sys.argv[1:], "d:")
    targetDir = ""
    for op, value in opts:
        if op == "-d":
            targetDir = value
            break

    #扫描目录
    if os.path.isdir(targetDir) == True:
        print('[*] 正在扫描 ' + targetDir + '\n')
        listfile = os.listdir(targetDir)
        videoType = (".avi",".mkv",".mp4",".rmvb",".rm",".m4v",".wmv")
    	for filename in listfile:
            [mid,nameActor] = _getMovieId(filename)
            fullFile = targetDir + os.path.sep + filename
            #清理原文件
            if os.path.isdir(fullFile) == True and fullFile != DUMP_DIR and filename[0:1] != ".":
                innerListfile = os.listdir(fullFile)
                for innerFile in innerListfile:
                    (shortname,fileExt) = _getFileNameAndExt(innerFile)
                    #隐藏文件和下载中的文件
                    if innerFile[0:1] == "." or fileExt[1:10] == "115chrome" or fileExt == '.cfg':
                        pass
                    elif fileExt in videoType:
                        pass
                    else:
                        print("[*]处理非视频文件 " + innerFile)
                        shutil.move(fullFile + os.path.sep + innerFile, DUMP_DIR + os.path.sep  + innerFile)
                #下载封面
                (imageSrc,actors) = getCoverUrlById(mid);
                if imageSrc != "":
                    _downloadImg(imageSrc,fullFile + os.path.sep + "cover.jpg")
                #修改文件名
                if nameActor == "" and actors != []:
                    print("rename "+ fullFile + " " + ",".join(nameActor))
                    # os.rename(fullFile,fullFile + " " + ",".join(s))
            else:
                pass
    else:
        print('[*]未找到目录，退出程序\n')
        exit()

    # print(getCoverUrlById("BF-366"))


if __name__ == '__main__':
    main()
