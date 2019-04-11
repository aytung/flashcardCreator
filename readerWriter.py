import csv
import webParsingFunctions
import dataProcessingFunctions
from dataProcessingFunctions import ResultPageType

def getDefinitionSentences(searchResult, defPageType):
	if dataProcessingFunctions.isWordPage(searchResult):
		return dataProcessingFunctions.getDefinitionSentences(searchResult, defPageType)	

	definitionLink =  dataProcessingFunctions.getDefinitionLink(furigana + kanji, searchResult)
	newResult = webParsingFunctions.getDefinitionPage(definitionLink)
	newResult = webParsingFunctions.getSoup(newResult)
	defPageType = dataProcessingFunctions.getResultPageType(newResult)
	return dataProcessingFunctions.getDefinitionSentences(newResult, defPageType)

def normalizeSentences(sentences):
	if not sentences:
		return sentences

	tempSentences = set()
	for sentence in sentences:
		if type(sentence) is list:
			for element in sentence:
				if element not in tempsentences:
					tempsentences.add(element)
		else:
			if sentence not in tempSentences:
				tempSentences.add(sentence)

	sentences = list(tempSentences)
	sentences = [sentence.strip() for sentence in sentences]
	sentences = [sentence for sentence in sentences if sentence]
	return sentences

def substituteWord(sentences, kanji, word):
	if not sentences:
		return sentences
	for index in range(0, len(sentences)):
		sentence = sentences[index]
		if kanji in sentence:
			sentences[index] = sentence.replace(kanji, " " + word).strip()
		else:
			if "―・" in sentence:
				sentences[index] = sentence.replace("―・", " " + word).strip()
			elif "―" in sentence:
				sentences[index] = sentence.replace("―", " " + word).strip()
	return sentences

def writeDefinitions(definitions, writer):
	if definitions:
		for definition in definitions:
			# print(definition)
			writefile.write(definition.strip())
			writefile.write('\n')

def writeSentences(sentences, writer):
	if sentences:
		for sentence in sentences:
			writefile.write(sentence.strip())
			writefile.write('\n\n')

with open('words.txt', 'r') as readfile, open('anki.txt', 'w') as writefile, open('error.txt', 'w') as errorfile:
	for cur_line in readfile:
		if not cur_line.strip():
			continue 
		print(cur_line)	
		kanji, furigana = dataProcessingFunctions.getWordFurigana(cur_line)
		searchResult = webParsingFunctions.getSearchResults(kanji)
		defPageType = dataProcessingFunctions.getResultPageType(searchResult)
		if defPageType == ResultPageType.NORESULT:
			#errorfile.writerow(cur_line)
			print('invalid word')
			errorfile.write(cur_line)
			continue 

		try:
			definitions, sentences = getDefinitionSentences(searchResult, defPageType)

			word = cur_line.strip()

			definitions = normalizeSentences(definitions)
			sentences = normalizeSentences(sentences)
			sentences = substituteWord(sentences, kanji, word)
			writefile.write(word.strip())

			writeDefinitions(definitions)
			writefile.write('\n')
			writeSentences(sentences)
		except:
			print("ERROR: " + cur_line.strip())
			import pdb; pdb.set_trace()
			print()
			writefile.write("TODO: " +  cur_line)

	readfile.close()
	writefile.close()
	errorfile.close()
