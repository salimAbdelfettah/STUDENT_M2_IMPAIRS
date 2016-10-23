import re, string, datetime
from unidecode import unidecode
from array import array

class Utils(object):

	
	oddWords = ["de", "du", "la", "le", "a", "au", "aux", "les", "nos",
					 "mon", "mes", "pour", "en", "ou", "et", "son", "par",
					 "d'", "l'", "y", "sur", "mais", "donc", "or", "ni", "car"]
	substitute = r'\(d\'|l\'|[^)]*\)|[0-9]+|['+string.punctuation+']+'

	@staticmethod
	def formatSentence(text):
		text = re.sub(Utils.substitute, " ", unidecode(text).lower())
		#text = ' '.join([m for m in (text.split(" ")) if m not in Utils.oddWords])
		return text

	@staticmethod
	def formatWord(text):
		text = unidecode(text)
		text = re.sub(r'(d\'|l\')', "", text)
		text = re.sub(r'(\s)+', " ", text)
		text = text.lower()
		return text

	@staticmethod
	def decodeAndMakeLowerATitle(text):
		text = unidecode(text)
		text = text.lower()
		return text

	@staticmethod
	def printWhenStarted():
		now = datetime.datetime.now()
		print "Started new action at : %d/%d/%d %d:%d:%d" % (now.year, now.month, now.day, now.hour, now.minute, now.second)
		del now

	@staticmethod
	def printWhenFinished():
		now = datetime.datetime.now()
		print "Finished action at : %d/%d/%d %d:%d:%d" % (now.year, now.month, now.day, now.hour, now.minute, now.second)
		del now

	@staticmethod
	def saveCLIMatrix(C, L, I, pathToFile):
		Utils.saveList(C, "%f", pathToFile, "C")
		Utils.saveList(L, "%d", pathToFile, "L")
		Utils.saveList(I, "%d", pathToFile, "I")

	@staticmethod
	def saveList(listContent, typeOfContent, pathToFile, ext):
  		print "Saving list ..."
  		typeOfContent = typeOfContent + "\n"
  		fileToWriteOn = open(pathToFile+'.'+ext,'w')
  		for item in listContent:
  			fileToWriteOn.write(typeOfContent % item)
  			del item
  		del fileToWriteOn
  		del typeOfContent
  		del ext
  		print "Saving list finished."

  	@staticmethod
  	def importList(fileName, typeOfContent, typeCode):
  		print "Importing list ..."
  		result = array(typeCode)
  		fileToRead = open(fileName, 'r')
		for line in fileToRead:
			result.append(typeOfContent(line.rstrip('\n')))
			del line
		del fileToRead
		print "List imported.", len(result)
		return result