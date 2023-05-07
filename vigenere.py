# Cifra de Vigenere
# Rodrigo Teixeira Soares 	19/0019760

import sys
import math

# This function is used to make operations using number representations of letters.
def letter_to_number(letter):
	return ord(letter) - 97

# This is used to retrieve a letter with a given number
def number_to_letter(number):
	return chr(number + 97)

# This function shifts a message to the right in 1 character
def shift_message(message):
	shifted_message = list(message)
	shifted_message[0] = ' '
	for i in range(len(message) - 1):
		shifted_message[i+1] = message[i]
	return shifted_message

# This function retrieves the most common item in a given list
def most_frequent(message):
    counter = 0
    num = message[0]
     
    for i in message:
        curr_frequency = message.count(i)
        if(curr_frequency> counter):
            counter = curr_frequency
            num = i
    return num

# This function tries to find a letter used to shift a given text, given the frequencies of the letters in that language.
# This matches the letters using the relative frequency of letters in the text and in the language.
def best_match(letters, letter_frequencies):
	best_letter = ''
	difference = 1.0
	best_percentage = 0.0
	found_frequencies = {}
	for i in range(len(letters)):
		count = 0
		for letter in letters:
			if letters[i] == letter:
				count+=1
		found_frequencies[letters[i]] = count/len(letters)
	shifts = []
	letter_frequencies = dict(list(letter_frequencies.items())[:len(found_frequencies)])
	while(len(letter_frequencies) > 0 and len(found_frequencies) > 0):
		difference = 1.0
		for letter in found_frequencies:
			for given_letter in letter_frequencies:
				if difference > abs(found_frequencies[letter] - letter_frequencies[given_letter]):
					difference = abs(found_frequencies[letter] - letter_frequencies[given_letter])
					best_letter = letter
					best_given_letter = given_letter
		letter_frequencies.pop(best_given_letter)
		found_frequencies.pop(best_letter)
		shift = (letter_to_number(best_letter) - letter_to_number(best_given_letter)) % 26
		shifts.append(shift)
	probable_letter = number_to_letter(most_frequent(shifts))
	return probable_letter

# This function tries to find a letter used to shift a given text, given the frequencies of the letters in that language.
# This matches the letters using the quantity of letters in the text and the frequencies of letters of the language.
def best_quantity(letters, letter_frequencies):
	shifts = []
	for letter in letter_frequencies:
		if (len(letters) > 0):
			found_letter = most_frequent(letters)
			shift = 0
			shift = (letter_to_number(found_letter) - letter_to_number(letter)) % 26
			shifts.append(shift)
			letters = [i for i in letters if i != found_letter]
	probable_letter = ''
	probable_letter = number_to_letter(most_frequent(shifts))
	return probable_letter

# This function cyphers a given message
def cypher(message, key):
	print("Cyphering...")
	result  = []
	key_index = 0
	message = message.lower()
	for i in range(len(message)):
		if (message[i] == ' '):
			result.append(' ')
		else:
			result.append(number_to_letter((letter_to_number(message[i]) + letter_to_number(key[key_index])) % 26))
			key_index = key_index + 1
			if (key_index >= len(key)):
				key_index = 0
	print("Cypher complete!")
	return ''.join(result)

# This function decyphers a given message
def decypher(message, key):
	print("Decyphering...")
	result  = []
	key_index = 0
	message = message.lower()
	for i in range(len(message)):
		if (ord(message[i]) < 97 or ord(message[i]) > 122):
			result.append(message[i])
		else:
			result.append(number_to_letter((letter_to_number(message[i]) - letter_to_number(key[key_index])) % 26))
			key_index = key_index + 1
			if (key_index >= len(key)):
				key_index = 0

	print("Decyphering complete!")
	return ''.join(result)

# This function breaks the cypher of a given message in a given language
def break_cypher(message, language='ptbr'):
	# Removing special characters
	message = message.lower()
	original_message = message
	special_characters = []
	for i in range(len(message)):
		if (ord(message[i]) < 97 or ord(message[i]) > 122):
			if message[i] not in special_characters:
				special_characters.append(message[i])
	for character in special_characters:
		message = message.replace(character, '')
	# Getting key length
	coincidences = []
	shifted_message = message
	for i in range(len(message)):
		shifted_message = shift_message(shifted_message)
		coincidence = 0
		for j in range(len(message)):
			if (message[j] == shifted_message[j]):
				coincidence = coincidence + 1
		coincidences.append(coincidence)
	key_length = 1
	best_key_length = 1
	best_average = 0
	averages = {}
	for i in range(int(len(message)/2)):
		average = 0
		for j in range(30):
			if (len(coincidences) > (((j+1)*key_length)-1)):
				average += coincidences[(((j+1)*key_length)-1)]
		averages[key_length] = average
		key_length += 1
	
	best_key = max(averages, key=averages.get)
	print("Best average of coincidences is for key length:" + str(best_key))
	# Separate letters into best_key bins
	decyphered = False
	strategies = ["quantity", "frequency"]
	curr_strategy = 0
	while not decyphered:
		frequent_letters = []
		if (language == 'en'):
			frequent_letters = {'e':0.13,'t':0.091,'a':0.082,'o':0.075,'i':0.07,'n':0.067,'s':0.063,'h':0.061,'r':0.06,'d':0.043,'l':0.04,'c':0.028,'u':0.028,'m':0.024,'w':0.024,'f':0.022,'g':0.02,'y':0.02,'p':0.019,'b':0.015,'v':0.0098,'k':0.0077,'j':0.0015,'x':0.0015,'q':0.00095,'z':0.00074}
		elif (language == 'ptbr'):
			frequent_letters = {'a':0.14634,'e':0.1257,'o':0.09735,'s':0.06805,'r':0.0653,'i':0.06186,'d':0.04992,'m':0.04738,'n':0.04446,'t':0.04336,'c':0.03882,'u':0.03639,'l':0.02779,'p':0.02523,'v':0.01575,'g':0.01303,'q':0.01204,'b':0.01043,'f':0.01023,'h':0.00781,'z':0.0047,'j':0.00397,'x':0.00253}
		bins = {}
		for i in range(len(message)):
			if i%best_key not in bins:
				bins[i%best_key] = []
			bins[i%best_key].append(message[i])
		guessed_key = []
		bin_letter_index = 1
		for key_letter in bins:
			print("Guessing letter " + str(bin_letter_index))
			found_letter = ''
			if (strategies[curr_strategy] == "quantity"):
				found_letter = best_quantity(bins[key_letter], frequent_letters.keys())
			elif (strategies[curr_strategy] == "frequency"):
				found_letter = best_match(bins[key_letter], frequent_letters)
			print("Probable letter in this bin: " + found_letter)
			guessed_key.append(found_letter)
			bin_letter_index += 1
		print("Guessed Key: " + ''.join(guessed_key))
		guessed_message = decypher(original_message, guessed_key)
		print("Guessed message: " + guessed_message)
		prompt = input("Is it decyphered? y - Yes, n - No\n")
		if (prompt == 'y'):
			decyphered = True
			print("Code successfully decyphered. Key: " + ''.join(guessed_key))
			return (guessed_message, ''.join(guessed_key))
		else:
			if (curr_strategy+1 < len(strategies)) :
				curr_strategy += 1
				print("Trying again with a different strategy...")
			
			else:
				print("Ran out of strategies, break failed!")
				return ('', '')
		





# vigenere.py c/d/b message.txt key.txt result.txt ptbr/en
if (len(sys.argv) != 6 and len(sys.argv) != 5):
	raise Exception("Invalid arguments!")

operation = sys.argv[1] 
message_file = sys.argv[2]
key_file = sys.argv[3]
result_file = sys.argv[4]
language = 'ptbr'
if (len(sys.argv) == 6):
	language = sys.argv[5]
message = ""
key = ""
result = ""
with open(message_file) as f:
	message = f.read()

if (operation == "c"):
	with open(key_file) as f:
		key = f.read()
	result = cypher(message, key)

	# Saving to file
	with open(result_file, "w") as f:
		f.write(result)	

elif (operation == "d"):
	with open(key_file) as f:
		key = f.read()
	result = decypher(message, key)

	# Saving to file
	with open(result_file, "w") as f:
		f.write(result)	
		
elif (operation == "b"):
	(result, key) = break_cypher(message, language)

	# Saving key to file
	with open(key_file, "w") as f:
		f.write(key)	
	
	# Saving to file
	with open(result_file, "w") as f:
		f.write(result)
else:
	raise Exception("Invalid operation!")
