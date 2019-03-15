import bs4 as bs 
from urllib.request import Request, urlopen
from urllib.parse import quote


def getSoup(url):
	# site = 'https://dictionary.goo.ne.jp/jn/'
	hdr = {'User-Agent': 'Mozilla/5.0'}
	req = Request(url, headers=hdr)
	page = urlopen(req)
	soup = bs.BeautifulSoup(page, 'lxml')

	return soup

def isInvalidWord(soup):
	# TODO: write logic for detecting invalid webpage
def getSearchResults(word):
	percentEncoding = urllib.parse.quote(word)
	wordUrl = 'https://dictionary.goo.ne.jp/srch/jn/' + percentEncoding + '/m0u/'
	return getSoup(wordUrl)

def getDefinitionLink(origKanji, origReading, soup):
	longestMatch = 0
	longestLink = None
	for definition in definitions:
		# TODO: whenever the entire character is a set phrase
		# find the pronunciation and definition
		dictReading, dictKanji = definition.dt.text.split("【")
		# want to remove last character
		dictKanji = dictKanji[:-1]	 
		dictReading = "".join(dictReading.split("‐"))
		dictLink = definition.a.get('href')

		# dictReadings = "".join(dictReadings.split("-"))
		#import pdb; pdb.set_trace()
		dictMatch = 0 
		dictMatch += longestMatchingSubsequence(dictKanji, origKanji)
		dictMatch += longestMatchingSubsequence(origReading, dictReading)
		if dictMatch > longestMatch:
			longestMatch = dictMatch 
			longestLink = dictLink 

	return longestLink



