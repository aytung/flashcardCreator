import csv

# determines whether or not the card is a sentence
is_sentence = lambda line : line and line[0] == "「" and line[-1] == "」"



with open('anki.txt', 'r') as readfile, open('anki.csv', 'w') as writefile:
	writer = csv.writer(writefile, quoting=csv.QUOTE_MINIMAL)

	# the fields of the dictionary cards are of the form "front, back"
	# not necessary, though
	#writer.writerow(["Front","Back"])


	definition = None 
	dict_card = None

	for cur_line in readfile:
		# if it is a sentence, immediately write it
		if is_sentence(cur_line.strip()):
			writer.writerow([cur_line[:-1], None])
		# when this happens, we need to write a definition card
		elif cur_line == "\n" and dict_card:
			if definition:
				definition = definition[:-1]
			dict_card.append(definition)
			writer.writerow(dict_card)
			dict_card = None
		# define definition or add more
		elif dict_card:
			if not definition:
				definition = cur_line
			else:
				definition += cur_line
		# means that we need to add a new dictionary entry
		elif cur_line != "\n":
			definition = None
			dict_card = [cur_line[:-1]]

	readfile.close()
	writefile.close()
