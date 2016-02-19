# change number of repetiotion to bi

def parse_question(whole_question, question_strings, question_strings_np):
	return find_noun_phrases_in_question(whole_question, question_strings, question_strings_np)

def parse_repetition(whole_question, question_strings, question_strings_np):
	return find_repeated_noun_phrases(whole_question, question_strings_np)
	# find_useful_noun_phrases_in_question(noun_phrases_in_question, question_strings_np, question_strings)
def find_repeated_noun_phrases(whole_question, question_strings_np):
	repeated_noun_phrases = []
	for noun_phrase in question_strings_np:
		# print noun_phrase
		# if noun_phrase == "4 point":
		# 	print "heres"
		# print question_strings_np
		found_index = whole_question.find(noun_phrase) + 1
		if whole_question.find(noun_phrase, found_index) > -1:
			if noun_phrase not in repeated_noun_phrases:
				repeated_noun_phrases.append(noun_phrase)
	return repeated_noun_phrases
def find_related_np_to_conjucated_np(np1, np2, noun_phrase_list):
	res_list = []
	# print "cheeeck extra"
	# print np1
	# print np2
	for i in range(0, len(noun_phrase_list)):
		if noun_phrase_list[i].startswith(np1):
			ending_part = noun_phrase_list[i][len(np1) + 1:]
			for j in range(0, len(noun_phrase_list)):
				if j==i:
					continue
				if noun_phrase_list[j].startswith(np2) and noun_phrase_list[j].endswith(ending_part):
					if noun_phrase_list[j] not in res_list:
						res_list.append(noun_phrase_list[j])
						break
		elif noun_phrase_list[i].startswith(np2):
			ending_part = noun_phrase_list[i][len(np2) + 1:]
			for j in range(0, len(noun_phrase_list)):
				if j==i:
					continue
				if noun_phrase_list[j].startswith(np1) and noun_phrase_list[j].endswith(ending_part):
					if noun_phrase_list[j] not in res_list:
						res_list.append(noun_phrase_list[j])
					break
		elif noun_phrase_list[i].endswith(np1):
			starting_part = noun_phrase_list[i][:-1*len(np1) -1]
			for j in range(0, len(noun_phrase_list)):
				if j==i:
					continue
				if noun_phrase_list[j].endswith(np2) and noun_phrase_list[j].startswith(starting_part):
					if noun_phrase_list[j] not in res_list:
						res_list.append(noun_phrase_list[j])
					break
		elif noun_phrase_list[i].endswith(np2):
			starting_part = noun_phrase_list[i][:-1*len(np2) -1]
			for j in range(0, len(noun_phrase_list)):
				if j==i:
					continue
				if noun_phrase_list[j].endswith(np1) and noun_phrase_list[j].startswith(starting_part):
					if noun_phrase_list[j] not in res_list:
						res_list.append(noun_phrase_list[j])
					break
	# print res_list
	return res_list


def find_related_words_with_conjunction(file_name, noun_phrases_in_question, noun_phrase_list):
	parse_file = open(file_name, 'r')
	parse_text = parse_file.readline()
	index = parse_text.find('[u\'conj_')
	words_realted_with_conjunction = []
	while index > -1:
		part_text = parse_text[index:parse_text.find(']', index+1)].lower()
		# print part_text
		parts = part_text.split(', u\'')
		for i in range(1, len(parts)):
			parts[i] = parts[i][:-1].lower()
		for i in range(1, len(parts)):
			for np in noun_phrases_in_question:
				if np.startswith(parts[i]) or np.endswith(parts[i]):
					for j in range(1, len(parts)):
						if j == i:
							continue 
						if parts[j] not in np:
							words_realted_with_conjunction.append(np[:np.find(parts[i])] + parts[j] + np[np.find(parts[i]) + len(parts[i]):])
							others_important = find_related_np_to_conjucated_np(parts[i], parts[j], noun_phrase_list)
							for noun_phrase in others_important:
								words_realted_with_conjunction.append(noun_phrase)
		index = parse_text.find('[u\'conj_', index+1)
	return words_realted_with_conjunction

def find_srl_args(demanded_arg, question_strings_np, file_name):
	verb_related_np = []
	noun_phrases_in_demanded_arg = []
	input_file  = open(file_name, 'r')
	for line in input_file:
		line= line.lower()
		line = line[:-1]
		if line == "":
			continue
		parts = line.split(' ')
		if parts[1] == demanded_arg:
			rest_noun = ''
			for j in range(2, len(parts)-1):
				rest_noun = rest_noun + parts[j]  + ' '
			rest_noun = rest_noun + parts[len(parts)-1]
			if rest_noun not in noun_phrases_in_demanded_arg:
				noun_phrases_in_demanded_arg.append(rest_noun)
				verb_related_np.append(parts[0])
	return (noun_phrases_in_demanded_arg, verb_related_np)

def find_noun_phrases_in_question(whole_question, question_strings, question_strings_np):
	noun_phrases_in_question = []
	for i in range (0, len(question_strings)):
		sentence = question_strings[i].lower()
		if '?' in sentence or (i == len(question_strings) -1):
			for noun_phrase in question_strings_np:
				if sentence.find(noun_phrase) > -1:
					if noun_phrase not in noun_phrases_in_question:
						noun_phrases_in_question.append(noun_phrase.lower())
	return noun_phrases_in_question

def find_count_noun_stanford(file_name):
	noun_phrase_with_counts = []
	input_file = open(file_name, 'r')
	parse_text = input_file.readline()
	index = parse_text.find('(CD');
	while index >=0:
		parse_result = find_parsing_mode(file_name, index)
		parantese_index = parse_text.find('(', index + 1)
		if parse_result == 0:
			if parse_text[parantese_index+5: parse_text.find(')', parantese_index+1)] not in noun_phrase_with_counts:
				noun_phrase_with_counts.append(parse_text[parantese_index+5: parse_text.find(')', parantese_index+1)].lower())
		elif parse_result == 1:
			if parse_text[parantese_index+4: parse_text.find(')', parantese_index+1)] not in noun_phrase_with_counts:
				noun_phrase_with_counts.append((parse_text[index+4: parse_text.find(')', index)]+" "+parse_text[parantese_index+4: parse_text.find(')', parantese_index+1)]).lower())
		index = parse_text.find('(CD', index+1);
	return noun_phrase_with_counts

def find_parsing_mode(file_name, index):
		# this function looks for a type of the relation among the number and the noun_phrase.
		# here index is the index of founded '(CD' which is a refrence for the number
		parse_file = open(file_name, 'r')
		parse_text = parse_file.readline()
		next_open_parantese_index = parse_text.find('(', index + 1)
		# if parse_text[index-3: index-1] == 'NP':
		if parse_text[next_open_parantese_index + 1: next_open_parantese_index + 4] =='NNS':
			return 0
		elif parse_text[next_open_parantese_index + 1: next_open_parantese_index + 4] =='NN ':
			return 1
		elif parse_text[next_open_parantese_index + 1: next_open_parantese_index + 4] =='JJS': # for sit like 4 more then ...
			return 2
		elif parse_text[next_open_parantese_index + 1: next_open_parantese_index + 4] =='TO ':
			return 3
		else:
			return -1

def finding_if_noun_phrase_have_counts(np1):
	print "finding_if_noun_phrase_have_counts"

def read_disjoint_noun_phrase(file_name):
	res_disjoint_noun_phrases = []
	input_file = open(file_name, 'r')
	for line in input_file:
		line = line[:-1]
		if line == '':
			break
		parts = line.split('	')
		res_disjoint_noun_phrases.append(parts[0].lower())
		res_disjoint_noun_phrases.append(parts[1].lower())
	return res_disjoint_noun_phrases

def in_noun_phrases_in_list(list, noun_phrase):
	if noun_phrase in list:
		return 1;
	elif noun_phrase.endswith('es'):
		if noun_phrase[:-2] in list:
			return 1
	elif noun_phrase.endswith('s'):
		if noun_phrase[:-1] in list:
			return 1
	return 0

def check_if_disjoint(np1, np2, disjoint_noun_phrases):
	for i in range(0, len(disjoint_noun_phrases)/2):
		if np1 == disjoint_noun_phrases[i] or (np1.endswith('es') and np1[:-2] == disjoint_noun_phrases[i]) or (np1.endswith('s') and np1[:-1] == disjoint_noun_phrases[i]):
			if np2 == disjoint_noun_phrases[i + 1] or (np2.endswith('es') and np2[:-2] == disjoint_noun_phrases[i + 1]) or (np2.endswith('s') and np2[:-1] == disjoint_noun_phrases[i + 1]):
				return 1

		if np2 == disjoint_noun_phrases[i] or (np2.endswith('es') and np2[:-2] == disjoint_noun_phrases[i]) or (np2.endswith('s') and np2[:-1] == disjoint_noun_phrases[i]):
			if np1 == disjoint_noun_phrases[i + 1] or (np1.endswith('es') and np1[:-2] == disjoint_noun_phrases[i + 1]) or (np1.endswith('s') and np1[:-1] == disjoint_noun_phrases[i + 1]):
				return 1
	return -1


noun_phrase_with_counts = []
noun_phrases_in_question = []
repeated_noun_phrases = []
related_words_with_conjunction = []
noun_phrases_in_arg1 =[]
verb_related_np_arg1 =[]
verb_related_np_arg0 =[]
noun_phrases_in_arg0 =[]
disjoint_noun_phrases = []

if __name__ =="__main__":
	# if argv[1] == 'test':
	# 	print "test"
	if 1 == 1:
		output_file = open('test_features.txt', 'w')
		for i in range(35, 50):
			if i == 17 or i == 30 or i == 33:
				continue
			input_file = open("data/problems/" + str(i) + '.txt', 'r')
			whole_question = input_file.readline()
			disjoint_noun_phrases = read_disjoint_noun_phrase("data/disjoints/" + str(i) + '.dis')
			input_file = open("data/spilit/" + str(i) + '.txt.ssplit', 'r')
			question_strings = []
			for line in input_file:
				question_strings.append(line.lower())
			input_file = open("data/np/" + str(i) + '.txt.ssplit.ccg.nps','r')
 			question_strings_np = []
			for np in input_file:
				if np[-2] == ',' or np[-2] == '.' or np[-2] == '!' or np[-2] == '?':
					question_strings_np.append(np[:-3].lower())
				else:
					question_strings_np.append(np[:-1].lower())
			noun_phrases_in_arg1, verb_related_np_arg1= find_srl_args("arg1", question_strings_np, "data/easySrlOut.txt")
			print noun_phrases_in_arg1
			noun_phrases_in_arg0, verb_related_np_arg0= find_srl_args("arg0", question_strings_np, "data/easySrlOut.txt")
			noun_phrases_in_question = parse_question(whole_question, question_strings, question_strings_np)
			noun_phrase_with_counts = find_count_noun_stanford("data/stan/parse_stan_corenlp"+str(i)+".txt")
			repeated_noun_phrases = parse_repetition(whole_question, question_strings, question_strings_np)
			related_words_with_conjunction = find_related_words_with_conjunction("data/stan/parse_stan_corenlp"+str(i)+"story.txt", noun_phrases_in_question, question_strings_np)
			for np1 in question_strings_np:
				for np2 in question_strings_np:
					if np1 == np2:
						continue
					output_file.write(str(check_if_disjoint(np1, np2, disjoint_noun_phrases)) + ' ')
					output_file.write(str(in_noun_phrases_in_list(noun_phrases_in_arg0, np1)) + ' ')
					output_file.write(str(in_noun_phrases_in_list(noun_phrases_in_arg0, np2)) + ' ')
					output_file.write(str(in_noun_phrases_in_list(noun_phrases_in_arg1, np1)) + ' ')
					output_file.write(str(in_noun_phrases_in_list(noun_phrases_in_arg1, np2)) + ' ')
					output_file.write(str(in_noun_phrases_in_list(noun_phrase_with_counts, np1)) + ' ')
					output_file.write(str(in_noun_phrases_in_list(noun_phrase_with_counts, np2)) + ' ')
					output_file.write(str(in_noun_phrases_in_list(noun_phrases_in_question, np1)) + ' ')
					output_file.write(str(in_noun_phrases_in_list(noun_phrases_in_question, np2)) + ' ')
					output_file.write(str(in_noun_phrases_in_list(repeated_noun_phrases, np1)) + ' ')
					output_file.write(str(in_noun_phrases_in_list(repeated_noun_phrases, np2)) + ' ')
					output_file.write(str(in_noun_phrases_in_list(related_words_with_conjunction, np1)) + ' ')
					output_file.write(str(in_noun_phrases_in_list(related_words_with_conjunction, np2)) + ' \n')





