import math
from utils import Utils

class PageRank:

	def __init__(self, pathToFile, zap, precision):
		pathToFile = pathToFile.split('.xml')[0]
		self.zap = zap
		self.precision = precision
		Utils.printWhenStarted()
		print "Importing CLI matrix ..."
		self.C = Utils.importList(pathToFile+'.C', float, 'f')
		self.L = Utils.importList(pathToFile+'.L', int, 'I')
		self.I = Utils.importList(pathToFile+'.I', int, 'I')
		self.pathToFile = pathToFile
		del pathToFile
		print "CLI matrix Imported."
		Utils.printWhenFinished()
		print "C", len(self.C)
		print "L", len(self.L)
		print "I", len(self.I)

	def computePageRank(self):
		Utils.printWhenStarted()
		print "Computing page rank ..."
		self.numberOfPages = len(self.L) - 1
		self.DN = self.zap / self.numberOfPages
		self.D1 = 1. - self.zap
		initialValue = 1./self.numberOfPages
		P = []
		for index in range(self.numberOfPages):
			P.append(initialValue)
		del initialValue
		sigma = 1.0
		while(sigma > self.precision):
			oldP = P
			P = self.computeNewP(P)
			sigma = self.computeNewSigma(oldP, P)
			del oldP
		#print "P", P
		self.pageRank = P
		del P
		Utils.printWhenFinished()
		print "Computing page rank finished."

	def computeNewP(self, P):
		print "new Page Rank"
		newP = [0] * self.numberOfPages
		for indexJ in range(self.numberOfPages):
			if self.L[indexJ] != self.L[indexJ+1]:
				fromIndex = self.L[indexJ]
				toIndex = self.L[indexJ + 1]
				while fromIndex < toIndex:
					indexI = self.I[fromIndex]
					#print "J :", indexJ, "I :", indexI, "from :", fromIndex, "to :", toIndex
					newP [indexI] = newP [indexI] + (self.C[fromIndex] * P[indexJ])
					fromIndex = fromIndex + 1
					del indexI
				del fromIndex
				del toIndex
		for elem in newP:
			elem = self.DN + (self.D1 * elem)
		return newP

	def computeNewSigma(self, oldP, P):
		newSigma = 0
		for index in range(self.numberOfPages):
			newSigma = newSigma + math.fabs(oldP[index] - P[index])
		print "Sigma", newSigma
		return newSigma

	def getValueAt(self, fromIndex, toIndex, indexToFind):
		#print "getValueAt", indexToFind
		found = False
		index = fromIndex
		while not found and index < toIndex:
			if self.I[index] == indexToFind:
				found = True
			else:
				index = index + 1
		if index == toIndex:
			return None
		else:
			#print "theValue", self.C[index]
			return self.C[index]

	def sortePagesByPageRank(self):
		Utils.printWhenStarted()
		print "Sorting pages and ranks ..."
		pageAndRank = []
		for index in range(self.numberOfPages):
			pageAndRank.append([index, self.pageRank[index]])
		pageAndRank = sorted(pageAndRank, key=lambda tup: tup[1], reverse=True)
		pages = [page[0] for page in pageAndRank]
		ranks = [page[1] for page in pageAndRank]
		Utils.saveList(pages, "%d", self.pathToFile, "pages")
		Utils.saveList(ranks, "%f", self.pathToFile, "ranks")
		del pageAndRank
		del pages
		del ranks
		Utils.printWhenFinished()
		print "Pages and ranks sorted."