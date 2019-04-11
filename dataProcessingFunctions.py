import re 

exampleRegexp = re.compile(r"""「.*」""")

parenRegexp = re.compile(r"""（.*）""")
furiganaRegexp = re.compile(r"""\[.*\]""")
from enum import Enum
class ResultPageType(Enum):
	NORESULT = 0
	COMPLEXWORDPAGE = 1
	SIMPLEWORDPAGE = 2
	DEFPAGE = 3 
	ALTWORDPAGE = 4
# Determine whether the page has a box contaning a meaning_area,
# Which typically contains definitions
def isWordPage(soup):
	return len(soup.findAll('div', {'class' : 'contents_area meaning_area cx'})) != 0

# Determines whether or not the web page contains more than one definition
def isComplexWordPage(soup):
	# return len(soup.find_all('ol', {'class' : 'meaning cx'})) != 0
	return len(set([element.text.strip() for element in soup.find_all('ol', {'class' : 'meaning cx'})])) >= 2

# Determines whether the word page is not a complex work page or a simple word page
# Determines whether or not the page has 
def isAlternativeWordPage(soup):
	# import pdb; pdb.set_trace()
	# import pdb; pdb.set_trace()
	contentArea = soup.find('div', {'class' : 'contents_area meaning_area cx'})
	if contentArea:
		if contentArea.find('div', {'class' : 'text'}):
			return True
	return False

def isErrorPage(soup):
	return len(soup.findAll('div', {'class' : 'section contents-wrap-a-in search lead'})) != 0
def getResultPageType(soup):
	if isWordPage(soup):
		if isComplexWordPage(soup):
			return ResultPageType.COMPLEXWORDPAGE
		if isAlternativeWordPage(soup):
			return ResultPageType.ALTWORDPAGE
		else:
			return ResultPageType.SIMPLEWORDPAGE
	elif isErrorPage(soup):
 		return ResultPageType.NORESULT
	else:
		return ResultPageType.DEFPAGE 

def joinDefinitions(definitions):
	return "\n".join(definitions)
def getWordFurigana(word):
	sections = word.strip().split(' ')

	furiganaSection = []
	wordSection = []
	for section in sections:
		if furiganaRegexp.search(section):
			word = section[:furiganaRegexp.search(section).start()]
			furigana = furiganaRegexp.findall(section)[0]

			wordSection.append(section.replace(furigana, ""))
			furigana = furigana[1:-1]
			furiganaSection.append(furigana)
		else:
			wordSection.append(section)


	return "".join(wordSection), "".join(furiganaSection)

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

def getDefinitionLink(word, soup):
	longestMatchLength = float("inf")
	longestMatch = 0
	longestLink = None

	links = soup.find('ul', {'class' : 'list-search-a'})
	definitions = links.find_all('li')
	for fullDefinition in definitions:
		definition = fullDefinition.dt.text
		print(definition)

		while parenRegexp.findall(definition):
			definition = "".join(parenRegexp.split(definition))
			# definitions = definition.replace(parenRegexp)

		if "(" in definition or ")" in definition:
			continue
		dictReading, dictKanji = "", ""
		if "【" in definition:
			dictReading, dictKanji = definition.split("【")
		else:
			dictReading = definition
		dictKanji = dictKanji.strip()
		dictReading = "".join(dictReading.split("‐"))
		dictLink = fullDefinition.a.get('href')
		print("kanji", dictKanji, "reading", dictReading)
		dictMatch = longestMatchingSubsequence(dictReading + dictKanji, word)
		definitionLength = len(dictReading) + len(dictKanji)
		print("dictmatch", dictMatch)
		print("definitionlength", definitionLength)

		if dictMatch > longestMatch or longestMatchLength > dictMatch and dictMatch == longestMatch:
			longestMatch = dictMatch 
			longestLink = dictLink 
			longestMatchLength = definitionLength 

	print(longestLink)
	return longestLink




import re 

exampleRegexp = re.compile(r"""「.*」""")

def replaceWithFurigana(sentences, kanji, kanjiWFurigana):
	for sentence in sentences:
		sentence.replace(kanji, kanjiWFurigana)

def getDefinitionSentences(soup, pageType):
	if pageType == ResultPageType.COMPLEXWORDPAGE:
		return getDefinitionSentencesComplex(soup)
	elif pageType == ResultPageType.ALTWORDPAGE:
		return getDefinitionSentencesAlt(soup)
	else:
		return getDefinitionSentencesSimple(soup)		

def getDefinitionSentencesSimple(soup):
	definitionBox = soup.find('div', {'class' : 'contents_area meaning_area cx' })

	print("definitionBox for simple", definitionBox.text)
	dictEntry = definitionBox.find('p', {'class' : 'text'}).text

	exampleSentences = []
	definition = []

	definition.append(exampleRegexp.split(dictEntry)[0])

	#exampleSentences.extend(re.findall(exampleRegexp, dictEntry))
	examples = re.findall(exampleRegexp, dictEntry)
	for example in examples:
		exampleSentences.extend(\
			['「' + sentence for sentence in example.split('「')\
			if sentence])

	return definition, exampleSentences

def getDefinitionSentencesAlt(soup):
	# return soup.find('div', {'class' : 'contents_area meaning_area cx'}).find('div', {'class' : 'text'}).text, ""
	textbox = soup.find('div', {'class' : 'contents_area meaning_area cx'})
	sentences = textbox.find('li')

	if sentences:
		sentences.extract()

	if textbox.p:
		textbox.p.extract()


	definition = textbox.text.strip()
	if sentences:
		sentences = sentences.text
		if '\n' in sentences:
			sentences = [sentence for sentence in sentences.split('\n') if sentence]
	else:
		sentences = ''
	if type(sentences) != list:
		return [definition], [sentences]

	return [definition], sentences



def getDefinitionSentencesComplex(soup):
	dictEntries = soup.find_all('ol', {'class' : 'meaning cx'})

	exampleSentences = []
	definition = []

	# import pdb; pdb.set_trace()


	for dictEntry in dictEntries:
		# if not (ord(dictEntry[1]) >= 65297 and ord(dictEntry[1]) <= 65305):
		# 	continue
		unwanted = dictEntry.find('p').find('strong')
		if unwanted:
			unwanted.extract()
		dictEntry = dictEntry.text
		definition.append(exampleRegexp.split(dictEntry)[0].strip())

		examples = re.findall(exampleRegexp, dictEntry)
		for example in examples:
			exampleSentences.extend(\
				['「' + sentence for sentence in example.split('「')\
				if sentence])
	return definition, exampleSentences





