#! /usr/bin/env python

import urllib,urllib2,re

class BDTB:

	def __init__(self, baseurl, seelz, floortag):
		self.baseurl = baseurl
		self.seelz = '?see_lz=' + str(seelz)
		self.tool = tool()
		self.file = None
		self.floor = 1
		self.title = "baidu_tieba"
		self.floortag = floortag
	def getpage(self, pagenum):
	    try:
		url = self.baseurl + self.seelz + '&pn=' + str(pagenum)
		request = urllib2.Request(url)
		response = urllib2.urlopen(request)
#		print response.read().decode('utf-8')
		return response.read().decode('utf-8')
	    except urllib2.URLError, e:
		if(hasattr(e, "reason")):
			print "sorry, we have met some problems to connect to baidu", e.reason
		return None
	def gettitle(self, page):
		pattern = re.compile('<h1 class="core_title_txt.*?>(.*?)</h1>', re.S)
		result = re.search(pattern, page)
		if result:
			return result.group(1).strip()
		else:
			return None
	def getpagenum(self,page):
		pattern = re.compile('<li class="l_reply_num.*?</span>.*?<span.*?>(.*?)</span>',re.S)
		result = re.search(pattern, page)
		if result:
			return result.group(1).strip()
		else:
			return None
	
	def getcontent(self, page):
		pattern = re.compile('<div id="post_content_.*?>(.*?)</div>',re.S) 
		contents = []
		items = re.findall(pattern, page)
		for item in items:
			content = "\n" + self.tool.replace(item) + "\n"
			contents.append(content.decode('utf-8'))
		return contents
	def setfiletitle(self, title):
		if title is not None:
			self.file = open(title + ".txt", "w+")
		else:
			self.file = open(self.title + ".txt", "w+")
	def writedata(self, contents):
		for item in contents:
			if self.floortag == '1':
				floorline = "\n" + str(self.floor) + u"----------------------------------------\n"
				self.file.write(floorline)
			self.file.write(item)
			self.floor += 1

	def start(self):
		indexpage = self.getpage(1)
		pagenum = self.getpagenum(indexpage)
		title = self.gettitle(indexpage)
		self.setfiletitle(title)
		if pagenum == None:
			print "URL out_date"
			return
		try:
			print "this post has " + str(pagenum) + " pages"
			for i in range(1, int(pagenum) + 1):
				print "writing " + str(i) + " page data"
				page = self.getpage(i)
				contents = self.getcontent(page)
				self.writedata(contents)
		except IOError, e:
			print "writing exception,reason" + e.message
		finally:
			print "complete"



class tool:
	removeimg = re.compile('<img.*?>| {7} |')
	removeaddr = re.compile('<a.*?>|</a>')
	replaceline = re.compile('<tr>|<div>|</div>|</p>')
	replacetd = re.compile('<td>')
	removepara = re.compile('<p.*?>')
	removebr = re.compile('<br><br>|<br>')
	removeextratag = re.compile('<.*?>')
	def replace(self, x):
		x = re.sub(self.removeimg, "", x)
		x = re.sub(self.removeaddr, "", x)
		x = re.sub(self.replaceline, "\n", x)
		x = re.sub(self.replacetd, "\t", x)
		x = re.sub(self.removepara, "\n  ", x)
		x = re.sub(self.removebr, "\n", x)
		x = re.sub(self.removeextratag, "", x)
		return x.strip()




print "Please input page number:"
baseURL = 'http://tieba.baidu.com/p/' + str(raw_input(u'http://tieba.baidu.com/p/'))
seelz = raw_input("only lz?1:0\n")
floortag = raw_input("write floortag?1:0\n")
bdtb = BDTB(baseURL, seelz, floortag)
bdtb.start()
