import requests
from bs4 import BeautifulSoup
from utils import Utils

class WebParser:

	def __init__(self, link):
		self.link = link
		self.wgetPage()

	# Part 1

	def wgetPage(self):
		self.page = requests.get(self.link)
		self.textPage = BeautifulSoup(self.page.text, "html.parser")

	def getPage(self):
		return self.textPage

	def computeDistinctWords(self):
		words = []
		tags = self.textPage.findAll("td")
		for tag in tags:
			if tag.a != None:
				word = Utils.formatWord(tag.string)
				if len(word) > 1 and word not in Utils.oddWords and word not in words:
					words.append(word)
				del word
			del tag
		del tags
		self.words = words
		self.sortedWords = sorted(words)
		print str(len(words))+" word(s) found when compute distinct words"
		del words

	def getWords(self):
		return self.words

	def getSortedWords(self):
		return self.sortedWords

	def writeSortedDistinctWordsOnFile(self, link):
		Utils.printWhenStarted()
		print "Writing sorted distict words (dict) ..."
		file=open(link+'.words','w')
		for item in self.sortedWords:
  			file.write("%s\n" % item)
  			del item
  		del file
  		Utils.printWhenFinished()
  		print "Writing sorted distict words finished."

  	# Part 2

  	def getWordsInPageByTag(self, theTag):
		words = []
		tags = self.getTagsInPageByTagAndClass(theTag)
		for tag in tags:
			#print tag.string
			if tag.string != None:
				splitedwords = Utils.formatSentence(tag.string).split(' ')
				for splitedword in splitedwords:
					if len(splitedword) > 1 and splitedword not in Utils.oddWords:
						words.append(splitedword)
			else:
				print tag.findAll("li")
		
		return words

	def getTagsInPageByTag(self, theTag):
		return self.getTagsInPageByTagAndClass(theTag, None)

	def getTagsInPageByTagAndClass(self, theTag, theClass):
		if theClass == None:
			return self.textPage.findAll(theTag)
		else:
			return self.textPage.findAll(theTag, theClass)

	@staticmethod
	def getWordsFromTags(theTags):
		words = []
		for tag in theTags:
			if tag.string != None:
				splitedWords = Utils.formatSentence(tag.string).split(' ')
				for splitedWord in splitedWords:
				    if len(splitedWord) > 1 and splitedWord not in Utils.oddWords:
					    words.append(splitedWord)
		print str(len(words))+" word(s) found when compute words for "+str(len(theTags))+" tag(s)"
		return words

	@staticmethod
	def getTagsFromTags(theTags, theTag):
		tags = []
		for tag in theTags:
			tags = tags + tag.findAll(theTag)
		print str(len(tags))+" tag(s) found when compute tags from "+str(len(theTags))+" tags looking for the tag "+theTag
		return tags