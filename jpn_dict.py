import bs4 as bs 
from urllib.request import Request, urlopen

import re 

exampleRegexp = re.compile(r"""「.*」""")

def longestMatchingSubsequence(str1, str2):
	row = [0 for _ in range(0, len(str1) + 1)]
	cache = [row[:] for _ in range(0, len(str2))]
	cache.append(row)

	for row in range(0, len(str2)):
		for col in range(0, len(str1)):
			if str2[row] == str1[col]:
				cache[row + 1][col + 1] = cache[row][col] + 1
			else:
				cache[row + 1][col + 1] = max(cache[row + 1][col], cache[row][col + 1])

	return cache[-1][-1]


links = soup.find('ul', {'class' : 'list-search-a'})
# has the pronunciation of the word and kanji
#links.a.get('href')
#links.a.dt
definitions = links.findAll('li')
# in order to find the best matching string, we find out which
# one has the most characters that match the reading 
# in order to do that, we find out the furigana, and then compare that to 
# the elements in front of them 
# when there are none, do nothing
# we also find the longest matching substring for the other characters 

# in this file:
# take in a definition, get the appropriate link
# 
from urllib.parse import quote

def getSoup(url):
	# site = 'https://dictionary.goo.ne.jp/jn/'
	hdr = {'User-Agent': 'Mozilla/5.0'}
	req = Request(url, headers=hdr)
	page = urlopen(req)
	soup = bs.BeautifulSoup(page, 'lxml')

	return soup

# TODO: split file into separate files for easier readability

# TODO: get a csv file, and then use that to call all of the appropriate functions in this file
def writeCard(card):
	# TODO: write the card
def getFlashcard(word):

	searchResults = getSearchResults(word)
	definitionLink = getDefinitionLink(word, searchResults)
	definition, exampleSentences = getDefinitionSentences 

	# TODO: find a way to substitute the values
	# TODO: unify the definitions into a single element
	# TODO: find out how to write the single element 

def getSearchResults(word):
	percentEncoding = urllib.parse.quote(word)
	wordUrl = 'https://dictionary.goo.ne.jp/srch/jn/' + percentEncoding + '/m0u/'
	return getSoup(wordUrl)

def getDefinitionLink(word, soup):

	origKanji = "運動"
	origReading = "".join(['うん', 'どう'])

	longestMatch = 0
	# dictLinks = None 
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

import re 

exampleRegexp = re.compile(r"""「.*」""")

def getDefinitionSentences(soup):
	dictEntries = soup.find_all('ol', {'class' : 'meaning cx'})

	exampleSentences = []
	definition = []

	



	for dictEntry in dictEntries:
		#import pdb; pdb.set_trace()
		dictEntry = dictEntry.text
		if not (ord(dictEntry[1]) >= 65297 and ord(dictEntry[1]) <= 65305):
			continue
		# keep track of the original word, and substitute appropriate strings 
		# find all of the definitions for each element
		# then, also find all of the corresponding sentences
		# return a list consisting of the definitions, and of the example sentences
		# has the pronunciation of the word and kanji
		# import pdb; pdb.set_trace()
		definition.append(exampleRegexp.split(dictEntry)[0].split(' ')[1])

		exampleSentences.extend(re.findall(exampleRegexp, dictEntry))

	return definition, exampleSentences





