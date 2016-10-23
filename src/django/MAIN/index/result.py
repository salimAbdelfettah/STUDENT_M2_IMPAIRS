import re
from utils import Utils
from array import array

class Result():

	def __init__(self, pathOfXMLfile):
		self.path = pathOfXMLfile.split('.xml')[0]
		print "Loading pagerank ..."
		pagesFile = open(self.path+'.pages', 'r')
		ranksFile = open(self.path+'.ranks', 'r')
		pagerank = {}
		for line in pagesFile:
			pageNumber = array('I')
			pageNumber.append(int(line.rstrip('\n')))
			hisRank = array('f')
			hisRank.append(float(ranksFile.readline().rstrip('\n')))
			pagerank[pageNumber[0]] = hisRank[0]
			del line
			del pageNumber
			del hisRank
		del pagesFile
		del ranksFile
		self.pagerank = pagerank
		del pagerank
		print "Pagerank loaded."
		print "Loading titles ..."
		titles = []
		titleFile = open(self.path+'.titles', 'r')
		for line in titleFile:
			line = line.split(":")[1]
			titles.append(line)
			del line
		self.titles = titles
		del titles
		print "Titles loaded."
		print "Loading words pages relation ..."
		wpFile = open(self.path+'.wp', 'r')
		wp = {}
		for line in wpFile:
			head, freqs = self.splitLine(line.rstrip('\n'))
			for freq in freqs:
				if head not in wp:
					wp[head] = array('I')
				wp[head].append(freq[0])
				del freq
			#print "Pages of word", head, "loaded."
			del line
			del head
			del freqs
		self.wp = wp
		del wp
		print "Words pages relation loaded."

	def getResultForRequest(self, request):
		print "Computing result for request :", request
		vote = 0
		words = Utils.formatSentence(request)
		wordsInDict = []
		pages = []
		indexOfWords = {}
		lengthOfWPs = {}
		for word in words:
			if word in self.wp:
				wordsInDict.append(word)
				indexOfWords[word] = 0
				lengthOfWPs[word] = len(self.wp[word])
			del word
		del words
		currentPage = -1
		currentRank = 1
		ended = False
		if len(wordsInDict) == 0:
			ended = True
			return 0, []
			print "Result available Code 0."
		else:
			if len(wordsInDict) == 1:
				ended = True
				return 1, self.convertPagesIdToTitles(self.wp[wordsInDict[0]])
				print "Result available Code 1."
		while not ended:
			for word in wordsInDict:
				indexOfWord = indexOfWords[word]
				if indexOfWord >= lengthOfWPs[word]:
					ended = True
				else:
					if not ended:
						tempPage = self.wp[word][indexOfWord]
						tempRank = self.pagerank[tempPage]
						if currentRank > tempRank :
							currentRank = tempRank
							currentPage = tempPage
							vote = 0
						else:
							while indexOfWord < lengthOfWPs[word] and tempPage != currentPage and tempRank >= currentRank:
								indexOfWord = indexOfWord + 1
								indexOfWords[word] = indexOfWord
								del tempPage
								del tempRank
								if indexOfWord < lengthOfWPs[word]:
									tempPage = self.wp[word][indexOfWord]
									tempRank = self.pagerank[tempPage]
								else:
									tempPage = 0
									tempRank = 0
							if indexOfWord >= lengthOfWPs[word]:
								ended = True
							else:
								if currentPage == tempPage:
									vote = vote + 1
									if vote == len(wordsInDict):
										pages.append(currentPage)
										vote = 0
										for theWord in wordsInDict:
											indexOfWords[theWord] = indexOfWords[theWord] + 1
								else:
									if tempRank < currentRank:
										currentRank = tempRank
										currentPage = tempPage
										vote = 0
						del tempPage
						del tempRank
		print "Result available Code 2."

		return 2, self.convertPagesIdToTitles(pages)

	def convertPagesIdToTitles(self, pages):
		print "Converting pages numbers to titles ..."
		titles = []
		for page in pages:
			titles.append(self.titles[page])
			del page
		print "Pages numbers converted to titles ..."
		return titles

	def splitLine(self, line):
		line = line.rstrip('\n').split(':')
		head = line[0]
		line = line[1]
		line = re.sub(r'(\[|\]|\(|\))', ",", line)
		values = line.split(',')
		del line
		freqs = []
		pageNumber = None
		for value in values:
			if len(value) > 0:
				if pageNumber == None:
					pageNumber = int(value)
				else:
					freq = [pageNumber, int(value)]
					freqs.append(freq)
					pageNumber = None
					del freq
		return head, freqs