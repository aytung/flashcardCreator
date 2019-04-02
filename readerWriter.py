import csv
import webParsingFunctions
import dataProcessingFunctions
from dataProcessingFunctions import ResultPageType
with open('words.txt', 'r') as readfile, open('anki.txt', 'w') as writefile, open('error.txt', 'w') as errorfile:

	# writer = csv.writer(writefile, quoting=csv.QUOTE_MINIMAL)

	
	# read line
	for cur_line in readfile:
		# if the current line is blank, skip it
		if not cur_line.strip():
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
			# if cur_line.strip() == "荒[あ]れる" or cur_line.strip() == "比[ひ] 較[かく]":
			#  	import pdb; pdb.set_trace()
		
			newResult = webParsingFunctions.getDefinitionPage(\
			dataProcessingFunctions.getDefinitionLink(furigana + kanji, searchResult))

			# writefile.write(dataProcessingFunctions.getDefinitionLink(furigana + kanji, searchResult))
			# except:
			newResult = webParsingFunctions.getSoup(newResult)
			defPageType = dataProcessingFunctions.getResultPageType(newResult)
			# if cur_line.strip() == "比[ひ] 較[かく]":
			# 	import pdb; pdb.set_trace()
			
			# import pdb; pdb.set_trace()	
			definitions, sentences = dataProcessingFunctions.getDefinitionSentences(newResult, defPageType)



		word = cur_line.strip()

		# TODO: make a function in order to do this automatically
		print(sentences)
		definitions = [definitions for definition in definitions if definition]
		if sentences:
			sentences = [sentence for sentence in sentences if sentence]

		if sentences:
			for index in range(0, len(sentences)):
				sentence = sentences[index]
				if "―・" in sentence:
					sentences[index] = sentence.replace("―・", " " + word).strip()
				elif "―" in sentence:
					sentences[index] = sentence.replace("―", " " + word).strip()
				else:
					if kanji:
						print("there is kanji: ", kanji, "word", word)
						print("sentence: ", sentence)
						sentences[index] = sentence.replace(kanji, " " + word).strip()
		print(word)
		print(definition)
		writefile.write(word.strip())
		writefile.write('\n')
		# TODO: figure out why sometimes result is not unique
		tempDefinitions = set()
		if type(definitions[0]) is list:
			for definition in definitions:
				if type(definition) is list:
					for element in definition:
						if element not in tempDefinitions:
							tempDefinitions.add(element)

			definitions = list(tempDefinitions)
		for definition in definitions:
			print(definition)
			writefile.write(definition)
			writefile.write('\n')

		writefile.write('\n')

		sentences = list(set(sentences))
		print(sentences)
		if sentences:
			for sentence in sentences:
				writefile.write(sentence.strip())
				writefile.write('\n\n')


	readfile.close()
	writefile.close()
	errorfile.close()
