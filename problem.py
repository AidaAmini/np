import entity
import os
from nltk.parse import stanford
import stanford_parser

entity_list = []
entity_chain = []
question_sentence = ""
problem_text = ""
quantity_list = []
# repeated_noun_phrases = []
# noun_phrases_in_question = []
useful_noun_phrases_in_question = []
noun_phrase_with_counts = []
verbs_list = []

def add_Entity(self, new_entity):
		self.entities.append(new_entity)
		# if new_entity.unit not in self.used_units:
		# 	self.used_units.append(new_entity.unit)
		# self.check_entity_chains(new_entity)

def check_entity_chains(self, new_entity):
	# check if the given entiry is somehow related to other entities:
	# first way is to check repetition of a word in the entities
	# second is to run the stanford corenlp and see if that helps with cored
	# third is to find 
	print "temp line"

def finding_noun_phrases_after_per(whole_question, ccg_parse):
	noun_phrases_after_per = []
	ccg_parse = ccg_parse.lower()
	index_per = ccg_parse.find(" per ")
	while index_per > -1:
		if ccg_parse[index_per-3 : index_per] != "pos":
			index_per = ccg_parse.find(" per ", index_per+1)
			continue
		noun_phrase_new = ""
		index_np = ccg_parse.find("<l n", index_per + 1)
		# print index_np
		while ccg_parse[index_np+4] == '/':
			noun_phrase_new = noun_phrase_new + ccg_parse[index_np+15:ccg_parse.find(" n/n>" , index_np + 15)]
			index_np = ccg_parse.find("(<l n", index_per + 1)
		if ccg_parse[index_np + 4] == ' ':
			noun_phrase_new = noun_phrase_new + ccg_parse[index_np+13:ccg_parse.find(" n>)" , index_np + 13)]
			if noun_phrase_new not in noun_phrases_after_per:
				noun_phrases_after_per.append(noun_phrase_new)
		index_per = ccg_parse.find(" per ", index_per + 1)

	return noun_phrases_after_per

def parse_question(whole_question, question_strings, question_strings_np):
	return find_noun_phrases_in_question(whole_question, question_strings, question_strings_np)

def parse_repetition(whole_question, question_strings, question_strings_np):
	return find_repeated_noun_phrases(whole_question, question_strings_np)
	# find_useful_noun_phrases_in_question(noun_phrases_in_question, question_strings_np, question_strings)

def find_useful_noun_phrases_in_question(noun_phrases_in_question, question_strings_np, question_strings):
	print "//TODO"

def find_if_np_has_quantifier(noun_phrase):
	print "//TODO"	

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

def parse_srl_output_sentence(sentence_parts, question_index, sentence_index):
	for i in range(0, len(sentence_parts)-1):
		sentence = sentence_parts[i]
		parts = sentence.split(' ')
		verb_name = parts[0]
		rest_noun = ''
		for j in range(2, len(parts)):
			rest_noun = rest_noun + text[j]
		if parts[1].startswith('arg'):
			make_entity_of_noun(rest_noun)
		new_verb = verb.verb(verb_name, sentence_index, question_index, None, None, False, False)
		for verb in verbs_list:
			if verb.check_equal(new_verb):
				if parts[1] == 'arg1':
					verb.add_subject(rest_noun)
				elif parts[1] == 'arg2':
					verb.add_object(rest_noun)



def make_entity_of_noun(rest_noun):
	print "rest_noun"

def parse_srl_file(file_name, question_index):
	input_file = open(file_name, 'r')
	text = input_file.readline()
	sentence_parts = []
	index = 0
	for text in input_file:
		sentence_parts.append(text.lower())
		if sentence_parts[len(sentence_parts) - 1] == '':
			parse_srl_output_sentence(sentence_parts, question_index, index)
			sentence_parts = []
			index = index + 1
		# while sentence_parts[len(sentence_parts)-1] != '':
		# 	sentence_parts.append(input_file.readline())



def calc_accuracy():
	true_pos = 0
	false_neg = 0
	false_pos = 0
	total_size = 0
	for i in range(0, 50):
		if i == 17 or i == 30 or i == 33:
			continue
		noun_phrases_in_question = []
		noun_phrase_with_counts = []
		repeated_noun_phrases = []
		answer_noun_phrases = []
		noun_phrases_after_per = []
		related_words_with_conjunction = []
		ans_file = open("data/ans/" + str(i) + '.ans')
		for line in ans_file:
			if line[-2] == ' ':
				answer_noun_phrases.append(line[:-2].lower())
			else:
				answer_noun_phrases.append(line[:-1].lower())	
		input_file = open("data/problems/" + str(i) + '.txt', 'r')
		whole_question = input_file.readline()
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
		input_file = open("data/ccg/" + str(i) + '.txt.ssplit.ccg','r')
		ccg_parse = ""
		text = input_file.readline()
		while text!="":
			ccg_parse = ccg_parse + text
			text = input_file.readline()
		noun_phrases_in_question = parse_question(whole_question, question_strings, question_strings_np)
		# print "hhhhhhhhoaishdkjagfjkahf.kjdsbfk.hsd,fsbkdmbf,sbdf,sbd,fbsldfbnlskf"
		noun_phrases_after_per = finding_noun_phrases_after_per(whole_question, ccg_parse)
		print noun_phrases_after_per
		noun_phrases_in_question_set = set(noun_phrases_in_question)
		repeated_noun_phrases = parse_repetition(whole_question, question_strings, question_strings_np)
		repeated_noun_phrases_set = set(repeated_noun_phrases)
		related_words_with_conjunction = find_related_words_with_conjunction("data/stan/parse_stan_corenlp"+str(i)+"story.txt", noun_phrases_in_question, question_strings_np)
		related_words_with_conjunction_set = set(related_words_with_conjunction)
		noun_phrase_with_counts = find_count_noun_stanford("data/stan/parse_stan_corenlp"+str(i)+".txt")
		noun_phrase_with_counts_set = set(noun_phrase_with_counts)
		retrieved = []
		# print "noun_phrases_in_question"
		# print noun_phrases_in_question
		# print "noun_phrase_with_counts"
		# print noun_phrase_with_counts
		# print "repeated_noun_phrases"
		# print repeated_noun_phrases
		# print "answer_noun_phrases"
		# print answer_noun_phrases
		for noun_phrase in noun_phrases_in_question_set:
			if noun_phrase not in retrieved:
				if noun_phrase in answer_noun_phrases:
					retrieved.append(noun_phrase)
					true_pos = true_pos + 1
				else:
					false_pos = false_pos + 1
		for noun_phrase in noun_phrases_after_per:
			if noun_phrase not in retrieved:
				if noun_phrase in answer_noun_phrases:
					retrieved.append(noun_phrase)
					true_pos = true_pos + 1
				else:
					false_pos = false_pos + 1
		for noun_phrase in related_words_with_conjunction_set:
			if noun_phrase not in retrieved:
				if noun_phrase in answer_noun_phrases:
					retrieved.append(noun_phrase)
					true_pos = true_pos + 1
				else:
					false_pos = false_pos + 1
		for noun_phrase in noun_phrase_with_counts_set:
			if noun_phrase not in retrieved:
				if noun_phrase in answer_noun_phrases:
					retrieved.append(noun_phrase)
					true_pos = true_pos + 1
				else:
					false_pos = false_pos + 1
		for noun_phrase in repeated_noun_phrases_set:
			if noun_phrase not in retrieved:
				if noun_phrase in answer_noun_phrases:
					retrieved.append(noun_phrase)
					true_pos = true_pos + 1
				else:
					flag = False
					false_pos = false_pos + 1
		# print "whole_question"
		# print whole_question
		# print "answer_noun_phrases"
		# print answer_noun_phrases
		# print "retrieved"
		# print retrieved
		# print "noun_phrases_in_question"
		# print noun_phrases_in_question_set
		# print "repeated_noun_phrases"
		# print repeated_noun_phrases_set
		# print "related_words_with_conjunction"
		# print related_words_with_conjunction_set
		# print "noun_phrase_with_counts"
		# print noun_phrase_with_counts_set
		total_size = total_size + len(answer_noun_phrases)
		del related_words_with_conjunction
		del noun_phrases_in_question[:]
		del noun_phrase_with_counts[:]
		del repeated_noun_phrases[:]
		del answer_noun_phrases[:]
	print (true_pos+ 0.0) / total_size
	print (true_pos + 0.0) / (true_pos + false_pos + 0.0)


def find_count_noun_stanford(file_name):
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

	# print noun_phrase_with_counts
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

if __name__ =="__main__":
	calc_accuracy()
	# find_count_noun_stanford("parse_stan_corenlp6.txt")
	# print noun_phrase_with_counts
	# input_file = open('2.txt','r')
	# whole_question = input_file.readline()
	# input_file = open('2.txt.ssplit','r')
	# question_strings = []
	# for line in input_file:
	# 	question_strings.append(line)
	# input_file = open('2.txt.ssplit.ccg.nps','r')
	# question_strings_np = []
	# for np in input_file:
	# 	if np[-2] == ',' or np[-2] == '.' or np[-2] == '!' or np[-2] == '?':
	# 		question_strings_np.append(np[:-3])
	# 	else:
	# 		question_strings_np.append(np[:-1])
	# parse_question(whole_question, question_strings, question_strings_np)
	# new_entity = entity.entity("hello",[],None, False,False)
	# print new_entity.name


	# os.environ['STANFORD_PARSER'] = '/Users/amini91/Downloads/stanford-corenlp-full-2015-12-09/stanford-corenlp-3.6.0.jar'
	# os.environ['STANFORD_MODELS'] = '/Users/amini91/Downloads/stanford-corenlp-full-2015-12-09/stanford-corenlp-3.6.0-models.jar'
	# dep_parser=stanford.StanfordParser(model_path='/Users/amini91/Downloads/stanford-corenlp-full-2015-12-09/stanford-corenlp-3.6.0-models/')
	# print [parse.tree() for parse in dep_parser.raw_parse("The quick brown fox jumps over the lazy dog.")]


