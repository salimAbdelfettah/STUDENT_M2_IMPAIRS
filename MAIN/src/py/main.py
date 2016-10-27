from process import Process
from pageRank import PageRank
from sortwp import SortWordsPagesRelation

# <-- Defs -->
XMLFileLink = "/home/netbook/frwiki-20151226-pages-articles-multistream.xml"
tempXML = "/media/ubuntu/0E7814037813E86B/Users/Mu/Documents/Mes fichiers/py/frwiki.xml"
testXML = "/home/netbook/Documents/test.xml"
workingOnXMLFile = tempXML
wordsListLink = "https://fr.wiktionary.org/wiki/Utilisateur:Darkdadaah/Listes/Mots_dump/frwiki/2016-02-03"

print "---> Starting program <---"

# compute words-pages relation
#words_pages = Process(wordsListLink, workingOnXMLFile)
#words_pages.startProcessing()

# compute page rank
#zap = 0.1
#precision = 0.0001
#page_rank = PageRank(workingOnXMLFile, zap, precision)
#page_rank.computePageRank()
#page_rank.sortePagesByPageRank()

# sort words pages realation by ranks
sort_wp = SortWordsPagesRelation(workingOnXMLFile)
sort_wp.sortWordsPagesRelation()

print "---> Hey ! It's time to take a look on the results ! <---"