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

def getFlashcard(word):

	searchResults = getSearchResults(word)
	definitionLink = getDefinitionLink(word, searchResults)
	definition, exampleSentences = getDefinitionSentences 

	# TODO: find a way to substitute the values
	# TODO: unify the definitions into a single element
	# TODO: find out how to write the single element 

import re 

exampleRegexp = re.compile(r"""「.*」""")

def getDefinitionSentences(soup):
	dictEntries = soup.find_all('ol', {'class' : 'meaning cx'})

	exampleSentences = []
	definition = []

	for dictEntry in dictEntries:
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





