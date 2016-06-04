import re
import nltk
import numpy as np
import sys
import operator
import random as r

class Grammer:

	def __init__(self):
		self.structure = ""
		self.length = 0
		self.tense = [] #Past/Present/Future
		self.person = [] #First/second/third person, singular/Plural
		pass
	def set_structure(self,s):
		self.set_structure = s
	def print_struct(self):
		print(self.structure)
	def print_all(self):
		print(self.structure)
		print(self.length)
		print(self.tense)
		print(self.person)

	def generalize(self):
		pass
	def format_file_out(self):
		pass


class Words():
	"""
	The main purpose of words will to be able to fill in the slots in grammer in such a way that makes sense.
	For this purpose each word will have several attributes, including the words seen in context (n-gram).
	Will have a sentiment analysis at some point, this will feed into grammer

	"""

	def __init__(self):
		self.word = ""
		self.bigram = {}
		self.before = {} #Dictionaries with the words and their frequencies for both before and after
		self.after = {}
		self.word_type = np.zeros(37) #Will be a list because a word can be used in different ways
		#word_type = [CC,CD,DT,EX,FW,IN,JJ,JJR,JJS,LS,MD,NN,NNP,NNPS,NNS,PDT,POS,PRP,PRP$,RB,RBR,RBS,RP,SYM,TO,UH,VB,VBD,VBG,VBN,VBP,VBZ,WDT,WP,WP$,WRB]
		#each word will have a row that will fit into a matrix of words and their types
		self.emote = 0 #Will be a float ranging from -1 to 1 where 0 is neutral, -1 is negative and 1 is positive

	def print_all(self):
		print(self.word)
		print(self.two_before)
		print(self.before)
		print(self.after)
		print(self.word_type)
		print(self.emote)
	def format_file_out(self):
		pass

class mimic():
	def __init__(self):
		self.struct = {} #Dictionary of the structures used and the number of times it has been seen
		
		self.struct_size = {}
		self.words_seen = {} #Only keeps track of the number of times 
		
		#these two dictionaries will be what will store the information for the word/grammer
		self.word_def = {} 
		self.struct_def = {}

		self.most_prob_noun = []
		self.word_count = 0 #Want to have a general count of every word in the corpus to find the probabilities of certain words.
		self.tense_count = 0
		self.avg_len = 0 #for average length, when updating, keep track of how many structures have been seen, and then multiply average by that then add by the new val and divide by the new total
		self.total_read = 0

	def readin(self):
		file_name = sys.argv[1]
		"""Read in a file with the with command and then pass it line by line into parse_sentance"""
		with open(file_name, encoding='utf-8') as f:
			for line in f:
				sentances = re.split('[.?!]', line)
				for sent in sentances:
					self.parse_sentance(sent)

	def parse_sentance(self,s):
		#Create the dictionary of Words with their respective parts of speech
		sentance = s
		sentance = re.sub(r'[^A-Za-z ]','',sentance)
		tokens =  nltk.word_tokenize(sentance)
		pos = nltk.pos_tag(tokens)
		store_sentance = "" #Stores the structure of the sentance
		"""First block deals with the individual words
		"""
		#Key is the word and val is its grammaical identification
		for key,val in pos:
			store_sentance += val + "-"
			tag = pos[tokens.index(key)][1]
			if key in self.words_seen:
				#print("Has been seen before")
				temp = self.words_seen[key]
				self.words_seen[key] = temp+1
			else:
				#print("First time seen")
				self.words_seen[key] = 1
				#word_only = re.sub(r'[^A-Za-z ]','',sentance)
				if(key.isalpha()):

					#print("Reach this statement")
					self.word_def[key] = self.define_word(key,sentance,tag)
		"""This second block deals with the grammatical structure
		"""
		key_len = len(store_sentance.split("-"))
		print(store_sentance.split("-"))
		if (key_len in self.struct):
			key = self.struct[key_len] 
			self.struct[key_len] = key+1
			pass
		else:
			self.struct[key_len] = 1
			self.struct_def[store_sentance] = self.define_grammer(store_sentance)
		self.total_read +=1
		#print(self.total_read)
	
	def define_grammer(self,s):
		"""
		Takes in a string that is the grammatical structure (VB-NN-...)
		Modifys all the values for the class of grammer for that specific structure.
		"""
		temp = Grammer()
		#mod statement - structure
		temp.structure = s
		rem = s.split("-")
		#rem.remove('')
		#mod statement - length
		temp.length = len(rem)
		#mod statement - tense
		for x in rem:
			if("VBN" in x ) or ("VBD" in x):
				#print("TRUE" + " " + x)
				temp.tense.append("PAST")
			if("will" in x):
				temp.tense.append("FUTURE")

		#mod statement - person

		return temp
		

	def define_word(self,key_word,s,tag):
		"""
		Set all the parameters for a word once it is first seen,
		Takes in the word that I want to make the instance of and
		"""
		temp = Words()
		#s = re.sub(r'[^A-Za-z ]','',s)
		temp.word = key_word
		sp = s.split(" ")
		#print("The split sentance that the key appears in")
		#print(sp)
		index = sp.index(key_word)
		#print(index)
		bi = ""
		if(index>=2):
			bi = sp[index-1]+" "+ sp[index]
			#print(bi)
		if(bi in temp.bigram):
			val = temp.bigram[bi]
			temp.bigram[bi] = val+1
		else:
			temp.bigram[bi] = 1
		prior = ""
		if(index>0):
			prior = sp[index] 
		if(prior in temp.before):
			v = temp.before[prior]
			temp.before[prior] = v+1
		else:
			temp.before[prior] = 0
		self.word_type_list(temp,tag)
		#temp.before =  #Dictionaries with the words and their frequencies for both before and after
		#temp.word_type.append(tag) #Will be a list because a word can be used in different ways
		temp.emote = 0
		return temp

	def sentiment(self,s):
		"""Returns an int from -1 to +1 based on the sentiment of a sentance
		This value will be used for both the sentiment of subjects, and structures
		"""
		pos_lex = ('great','good')
		neg_lex = ('disappoint','lie')
		no_lex = ('no','not','never')
		#These words will flip the value 
		pos_val = 0
		neg_val = 0
		for i in s:
			subj_seen_pos = False
			subj_seen_neg = False
		#I see a subjective word and naively add or subtract, next four steps will change this approach so its not so naive.
			ind = s.index(i)
			if (s in pos_lex):
				pos_val += 1
				subj_seen_pos = True
			if (s in neg_lex):
				neg_val += -1
				subj_seen_neg = True
		#Negations -- if there is a negation (no,not,etc) and is followed by a subjective word, will look at last 4 words and next 1
			prev = []
			if(subj_seen_pos or subj_seen_neg and ind-4 < 0):
				prev = s[:ind]
				prev.append(s[ind+1])
			elif(subj_seen):
				prev = s[ind-4:ind]
				prev.append(s[ind+1])
			for no in prev:
				if(no in no_lex and subj_seen_pos):
					pos_val -= 1;
				elif(no in no_lex and subj_seen_neg):
					neg_val -= 1

		#modifiers -- presence of words like very, super, extremely
		
		#Polarity shift -- Expressing and opinion (pos/neg) then flip

		#Subject opinion -- how does the speaker feel about the subject and nouns in the current sentance, this will be pulled from the dict
		#Will innfluence the final score that is output, and the final score will eventually 
		
		

		return val
	
	def word_type_list(self,W,tag):
		"""
		Pass in a word object, and the tag that was just seen with that word in the parsing stage and increment that point in the row for that word
		"""
		if(tag == "CC"):
			W.word_type[0] += 1
		elif(tag == "CD"):
			W.word_type[1] += 1
		elif(tag == "DT"):
			W.word_type[2] += 1
		elif(tag == "EX"):
			W.word_type[3] += 1
		elif(tag == "FW"):
			W.word_type[4] += 1
		elif(tag == "IN"):
			W.word_type[5] += 1
		elif(tag == "JJ"):
			W.word_type[6] += 1
		elif(tag == "JJR"):
			W.word_type[7] += 1
		elif(tag == "JJS"):
			W.word_type[8] += 1
		elif(tag == "LS"):
			W.word_type[9] += 1
		elif(tag == "MD"):
			W.word_type[10] += 1
		elif(tag == "NN"):
			W.word_type[11] += 1
		elif(tag == "NNP"):
			W.word_type[12] += 1
		elif(tag == "NNPS"):
			W.word_type[13] += 1
		elif(tag == "NNS"):
			W.word_type[14] += 1
		elif(tag == "PDT"):
			W.word_type[15] += 1
		elif(tag == "POS"):
			W.word_type[16] += 1
		elif(tag == "PRP"):
			W.word_type[17] += 1
		elif(tag == "PRP$"):
			W.word_type[18] += 1
		elif(tag == "RB"):
			W.word_type[19] += 1
		elif(tag == "RBR"):
			W.word_type[20] += 1
		elif(tag == "RBS"):
			W.word_type[21] += 1
		elif(tag == "RP"):
			W.word_type[22] += 1
		elif(tag == "SYM"):
			W.word_type[23] += 1
		elif(tag == "TO"):
			W.word_type[24] += 1
		elif(tag == "UH"):
			W.word_type[25] += 1
		elif(tag == "VB"):
			W.word_type[26] += 1
		elif(tag == "VBD"):
			W.word_type[27] += 1
		elif(tag == "VBG"):
			W.word_type[28] += 1
		elif(tag == "VBN"):
			W.word_type[29] += 1
		elif(tag == "VBP"):
			W.word_type[31] += 1
		elif(tag == "VBZ"):
			W.word_type[32] += 1
		elif(tag == "WDT"):
			W.word_type[33] += 1
		elif(tag == "WP"):
			W.word_type[34] += 1
		elif(tag == "WP$"):
			W.word_type[35] += 1
		elif(tag == "WRB"):
			W.word_type[36] += 1
		
	def generate_mimic(self):#self,code=0,noise=0):
		"""Different codes will corespond to different topics that could be talked about
			Codes: 0 = Random :: 1 = America :: 2 = China :: 
		"""
		if 1 in self.struct:
			del self.struct[1]
		most_used_struct = sorted(self.struct.items(), key = operator.itemgetter(1))
		most_used_words = sorted(self.words_seen.items(),key=operator.itemgetter(1))
		most_used_words = most_used_words#.reverse()
		print(most_used_words)
		mimic_string = ""
		#naive first attempt, will not be what I want, just for fun and proof of concept
		#change this from a random choice to a probability distribution
		struct_size_choice = most_used_struct[r.randint(0,len(most_used_struct)-1)][0]
		print(struct_size_choice)
		type_mat = []
		word_list_for_random = []
		for w in most_used_words:
			print(w)
			print(self.word_def[w[0]].word_type)
			word_list_for_random.append(w[0])
			type_mat.append(self.word_def[w[0]].word_type)
		chosen_len = 0
		temp_struct = None
		i = 0
		while chosen_len != struct_size_choice:
			rand_key = r.choice(list(self.struct_def.keys()))
			temp_struct = self.struct_def[rand_key]
			chosen_len = temp_struct.length
			print(temp_struct.length)
		print(temp_struct.structure)
		pos_list = temp_struct.structure.split("-")
		print(pos_list)
		pos_list.pop()
		current_pos = 0
		for loc in pos_list:
			tmp = Words()
			print(loc)
			self.word_type_list(tmp,loc)
			loc_arr = tmp.word_type
			rand_word = ''
			print("Array of current term :: \n {}".format(loc_arr))
			while current_pos == 0:
				#This loop will assign the most probable words to the positions needed.
				#Use latent semantic indexing to group words by its type?

				#Rando just to see if I can slot fill
				rand_word = word_list_for_random[r.randint(0,len(self.word_def)-1)]
				#print(rand_word)
				current_pos = self.word_def[rand_word].word_type
				
				current_pos = np.dot(current_pos,loc_arr)
				#print(current_pos)
			print("Matching word/loc found! {}".format(rand_word))
			mimic_string += rand_word + " "
			current_pos = 0
		return mimic_string

				


			

def main():
	test = mimic()
	test.readin()
	cont = 'y'
	while cont == 'y':
		mimTest = test.generate_mimic()
		print(mimTest)
		cont = input("Generate Another [y]/n\n")
if __name__ == '__main__':
	main()
