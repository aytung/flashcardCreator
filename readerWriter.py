import csv
import webParsingFunctions
import dataProcessingFunctions
from dataProcessingFunctions import ResultPageType
with open('anki.txt', 'r') as readfile, open('dict.txt', 'w') as writefile, open('error.txt', 'w') as errorfile:

	# writer = csv.writer(writefile, quoting=csv.QUOTE_MINIMAL)

	
	# read line
	for cur_line in readfile:
		# if the current line is blank, skip it
		if cur_line.strip() == "":
			continue 
		print(cur_line)	
		# get back a string consisting of the word, and furignana	
		kanji, furigana = dataProcessingFunctions.getWordFurigana(cur_line)

		# get the search result 
		searchResult = webParsingFunctions.getSearchResults(kanji)

		# deal with the corresponding page
		defPageType = dataProcessingFunctions.getResultPageType(searchResult)


		definition = None 
		sentences = None 
		# if cur_line.strip() == "比[ひ]率":
		# import pdb; pdb.set_trace()
		# if invalid word, then write to errorfile
		if searchResult == None:
			print("none result")
		if defPageType == ResultPageType.NORESULT:
			#errorfile.writerow(cur_line)
			print('invalid word')
			continue 
		elif dataProcessingFunctions.isWordPage(searchResult):
			definitions, sentences = dataProcessingFunctions.getDefinitionSentences(searchResult, defPageType)
		else:
			#definitions = webParsingFunctions.getSoup(definitionLink)
			# searchResult = None 
			# try:

			newResult = webParsingFunctions.getDefinitionPage(\
			dataProcessingFunctions.getDefinitionLink(furigana + kanji, searchResult))

			writefile.write(dataProcessingFunctions.getDefinitionLink(furigana + kanji, searchResult))
			# except:
			newResult = webParsingFunctions.getSoup(newResult)
			defPageType = dataProcessingFunctions.getResultPageType(newResult)

			definitions, sentences = dataProcessingFunctions.getDefinitionSentences(newResult, defPageType)



		word = cur_line.strip()

		for sentence in sentences:
			if "―" in sentence:
				sentence.replace("―", word) 
			elif "―・" in sentence:
				sentence.replace("―・", word)
			else:
				sentence.replace(kanji, word)
		print(word)
		print(definition)
		writefile.write(str(defPageType))
		writefile.write(word.strip())
		# TODO: deal with incorrect classification of wordpages as ALT when simple
		# TODO: find out how to parse the word pages when simple and sentence
		writefile.write('\n')
		for definition in definitions:
			writefile.write(definition.strip())
			writefile.write('\n')

		writefile.write('\n')

		print(sentences)
		for sentence in sentences:
			writefile.write(sentence.strip())
			writefile.write('\n\n')


	readfile.close()
	writefile.close()
	errorfile.close()
