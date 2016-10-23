import re
from lxml import etree
from collections import Counter
from webParser import WebParser
from bs4 import BeautifulSoup
from webParser import WebParser
from utils import Utils

class Process:

	dispatch = 100000
	tags = ["p", "div", "a", "table", "th", "tr", "td", "ul", "ol", "li", "h2", "h3"]
	searchLinkStr = "\[\[.*?\]\]"
	subLinkStr = "\[+|\]+"
	prefix = '{http://www.mediawiki.org/xml/export-0.10/}'
	#prefix = ''

	def __init__(self, wordsListLink, pathToFile):
		# get file path without ".xml"
		self.pathToFile = pathToFile.split('.xml')[0]
		# parse a web page to get words (dict)
		webParser = WebParser(wordsListLink)
		webParser.computeDistinctWords()
		webParser.writeSortedDistinctWordsOnFile(self.pathToFile)
		# init
		self.wordsOfDict = webParser.getSortedWords()
		del webParser
		self.pageIndex = 0
		self.initDict()

	def initDict(self):
		self.dict = {}
		for word in self.wordsOfDict:
			self.dict[word] = []
			del word

	def startProcessing(self):
		self.parseADumpFile(self.pathToFile+'.xml')

	def parseADumpFile(self, linkToDumpFile):
		#context = etree.iterparse(linkToDumpFile, tag=Process.prefix+'page')
		#self.computeAndSaveTitles(context)
		#del context
		#print str(self.numberOfPages)+" node(s) processed for the dump : "+linkToDumpFile+"."
		#context = etree.iterparse(linkToDumpFile, tag=Process.prefix+'page')
		#self.C = []
		#self.L = [0]
		#self.I = []
		#self.lastIndex = 0
		#self.iterOnPages(context, self.computeCLIMatrix, self.funcToApplyWhenCLIMatrixComputed)
		#del context
		context = etree.iterparse(linkToDumpFile, tag=Process.prefix+'page')
		self.iterOnPages(context, self.computeWordsPagesRelation, self.funcToApplyWhenWordsPagesRelationComputed)
		del context

	# Titles part
	def computeAndSaveTitles(self, context):
		titleFile=open(self.pathToFile+'.titles','w')
		decodedAndLowerTitles = {}
		Utils.printWhenStarted()
		pageIndex = 0
		print "Computing and saving titles ..."
		try:
			for _, elem in context:
				for child in elem:
					if child.tag == Process.prefix+'title' :
						titleFile.write("%d:%s\n" % (pageIndex, child.text.encode('utf8')))
						decodedAndLowerTitles[Utils.decodeAndMakeLowerATitle(child.text)] = pageIndex
					child.clear()
					del child
				pageIndex = pageIndex + 1
				elem.clear()
				for ancestor in elem.xpath('ancestor-or-self::*'):
					while ancestor.getprevious() is not None:
						del ancestor.getparent()[0]
				del elem
		except etree.XMLSyntaxError, e:
			print e
		self.numberOfPages = pageIndex
		self.decodedAndLowerTitles = decodedAndLowerTitles
		del decodedAndLowerTitles
		del pageIndex
		Utils.printWhenFinished()
		print "Titles saved."

	# Page parsing part
	def iterOnPages(self, context, funcToApply, funcToApplyWhenEnded):
		self.pageIndex = 0
		Utils.printWhenStarted()
		print "Iter on nodes ..."
		try:
			for _, elem in context:
				self.parseAPage(elem, funcToApply)
				elem.clear()
				for ancestor in elem.xpath('ancestor-or-self::*'):
					while ancestor.getprevious() is not None:
						del ancestor.getparent()[0]
				del elem
		except etree.XMLSyntaxError, e:
			print e
		if funcToApplyWhenEnded != None:
			funcToApplyWhenEnded()
		print "Iteration on ", self.pageIndex, "nodes finished."
		Utils.printWhenFinished()

	def parseAPage(self, page, funcToApply):
		for child in page:
			if child.tag == Process.prefix+'revision':
				for secondChild in child:
					if secondChild.tag == Process.prefix+'text':
						funcToApply(secondChild.text)
					del secondChild
			del child

	# functions to apply part
	def computeWordsPagesRelation(self, text):
		if text != None:
			content = Utils.formatSentence(text).split(' ')
			self.computeDistinctWords(content)
			del content
			self.addWordsToDict()
		self.pageIndex = self.pageIndex + 1
		if self.pageIndex % Process.dispatch == 0:
			print "+"+str(Process.dispatch)+" --> "+str(self.pageIndex)
			self.saveWordsPagesRelation(self.pageIndex/Process.dispatch)
			del self.dict
			self.initDict()

	def computeCLIMatrix(self, text):
		if text != None:
			self.computeLinksOfAPage(text)
			self.lastIndex = self.lastIndex + self.numberOfExternalLinks
			if self.numberOfExternalLinks != 0:
				val = 1./self.numberOfExternalLinks
				for currentLink in self.links:
					self.C.append(val)
					self.I.append(currentLink)
					if currentLink >= self.numberOfPages:
						print "ooh !", currentLink
					del currentLink
				del val
		self.L.append(self.lastIndex)
		self.pageIndex = self.pageIndex + 1

	# at the end functions to apply
	def funcToApplyWhenWordsPagesRelationComputed(self):
		if self.pageIndex % Process.dispatch != 0:
			print "+"+str(self.pageIndex % Process.dispatch)+" --> "+str(self.pageIndex)
			self.saveWordsPagesRelation((self.pageIndex/Process.dispatch)+1)
		del self.dict
		print "WP pages :", self.pageIndex

	def funcToApplyWhenCLIMatrixComputed(self):
		print "C =", len(self.C)
		print "L =", len(self.L)
		print "I =", len(self.I)
		Utils.saveCLIMatrix(self.C, self.L, self.I, self.pathToFile)
		del self.C
		del self.L
		del self.I
		print "CLI matrix pages :", self.pageIndex

	 # useful functions
	def computeDistinctWords(self, words):
		distinctWords = set()
		freqWords= {}
		for word in words:
			distinctWords.add(word)
			if word in freqWords:
				freqWords[word] = freqWords[word] + 1
			else:
				freqWords[word] = 1
			del word
		self.freqWords = freqWords
		self.distinctWords = list(distinctWords)
		del distinctWords
		del freqWords

	def addWordsToDict(self):
		for word in self.distinctWords:
			if word in self.dict:
				self.dict[word].append((self.pageIndex, self.freqWords[word]))
			del word

	def computeLinksOfAPage(self, content):
		links = re.findall(Process.searchLinkStr, content)
		theLinks = set() 
		for link in links:
			link = re.sub(Process.subLinkStr, "", link)
			if "|" in link:
				link = link.split("|")[0]
			decodedLink = Utils.decodeAndMakeLowerATitle(link)
			if decodedLink in self.decodedAndLowerTitles:
				theLinks.add(self.decodedAndLowerTitles[decodedLink])
			del link
		self.links = sorted(theLinks)
		self.numberOfExternalLinks = len(theLinks)
		del links
		del theLinks

	def saveWordsPagesRelation(self, part):
		print "Saving words pages relation ..."
		fileToWriteOn = open(self.pathToFile+'.wp.part'+str(part),'w')
		listOfWords = sorted(list(self.dict))
		for item in listOfWords:
  			fileToWriteOn.write("%s:[" % item)
  			freqs = self.dict[item]
  			for freq in freqs:
  				fileToWriteOn.write("(%d,%d)," % (freq[0],freq[1]))
  				del freq
  			del freqs
  			del item
  			fileToWriteOn.write("()]\n")
  		del part
  		del fileToWriteOn
  		del listOfWords
  		print "Saving words pages relation finished."