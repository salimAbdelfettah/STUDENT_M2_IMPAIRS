import os.path
import re
from utils import Utils

class SortWordsPagesRelation:

	def __init__(self, pathToFiles):
		self.pathToFiles = pathToFiles.split('.xml')[0]
		self.fileToWriteOn = open(self.pathToFiles+'.wp', 'w')
		pages = Utils.importList(self.pathToFiles+'.pages', int, 'I')
		fileWords = open(self.pathToFiles+'.words')
		words = []
		for line in fileWords:
			words.append(line.rstrip('\n'))
		self.words = words
		del words
		index = 1
		while os.path.isfile(self.pathToFiles+'.wp.part'+str(index)):
			index = index + 1
		self.numberOfWPFiles = index - 1
		del index
		index = 0
		pagesDict = {}
		for page in pages:
			pagesDict[page] = index
			index = index + 1
			del page
		del pages
		self.pages = pagesDict
		del pagesDict

	def sortWordsPagesRelation(self):
		Utils.printWhenStarted()
		print "Compute words pages relation sorted by ranks ..."
		wpFiles = []
		for index in range(self.numberOfWPFiles):
			wpFiles.append(open(self.pathToFiles+'.wp.part'+str(index+1)))
		for word in self.words:
			wordFreqs = []
			for wpFile in wpFiles:
				head, freqs = self.splitLine(wpFile.readline())
				if head != word:
					print "Head different from word.", head, word
				for freq in freqs:
					freq.append(self.pages[freq[0]])
					del freq
				wordFreqs = wordFreqs + freqs
				del freqs
			wordFreqs = sorted(wordFreqs, key=lambda tup: tup[2])
			self.writeWordPagesSortedByRanks(word, wordFreqs)
			#print word, ":", wordFreqs
			del word
			del wordFreqs
		Utils.printWhenFinished()
		print "Words pages relation sorted by ranks computed."

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

	def writeWordPagesSortedByRanks(self, word, freqs):
  		self.fileToWriteOn.write("%s:[" % word)
  		for freq in freqs:
  			self.fileToWriteOn.write("(%d,%d)," % (freq[0],freq[1]))
  			del freq
  		self.fileToWriteOn.write("()]\n")