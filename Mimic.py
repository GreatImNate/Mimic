import re
import nltk
import sys
import operator

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
		self.word_type = [] #Will be a list because a word can be used in different ways
		self.emote = 0 #Will be a float ranging from -1 to 1 where 0 is neutral, -1 is negative and 1 is positive

	def print_all(self):
		print(self.word)
		print(self.two_before)
		print(self.before)
		print(self.after)
		print(self.word_type)
		print(self.emote)

class mimic():
	def __init__(self):
		self.struct = {} #Dictionary of the structures used and the number of times it has been seen
		self.struct_size = {}
		self.words_seen = {}
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
				sentances = line.split(".")
				for sent in sentances:
					self.parse_sentance(sent)

	def parse_sentance(self,s):
		#Create the dictionary of Words with their respective parts of speech
		sentance = s
		sentance = re.sub(r'[^A-Za-z ]','',sentance)
		tokens =  nltk.word_tokenize(sentance)
		pos = nltk.pos_tag(tokens)
		store_sentance = "" #Stores the structure of the sentance
		#Key is the word and val is its grammaical identification
		print("The nltk tokens \n{}".format(pos))
		for key,val in pos:
			store_sentance += val + "-"
			print(key + " :: " + val)
			if key in self.words_seen:
				print("Has been seen before")
				temp = self.words_seen[key]
				self.words_seen[key] = temp+1


			else:
				print("First time seen")
				self.words_seen[key] = 1
				#word_only = re.sub(r'[^A-Za-z ]','',sentance)
				if(key.isalpha()):
					#print("Reach this statement")
					self.define_word(key,sentance)
				# -- will go here when the word is first seen and fill out all its
		print(store_sentance)
		print(self.words_seen)
		#need to implement an if statement to see if the grammer struct has been seen before, though much more unlikely than words, it is still possible
		if (store_sentance in self.struct):
			key = self.struct[store_sentance] 
			self.struct[store_sentance] = key+1
			pass
		else:
			self.struct[store_sentance] = 1
			self.define_grammer(store_sentance)
		self.total_read +=1
		print(self.total_read)
	
	def define_grammer(self,s):
		"""
		Takes in a string that is the grammatical structure (VB-NN-...)
		Modifys all the values for the class of grammer for that specific structure.
		"""
		temp = Grammer()
		#mod statement - structure
		temp.structure = s
		rem = s.split("-")
		rem.remove('')
		#mod statement - length
		temp.length = len(rem)
		#mod statement - tense
		for x in rem:
			if("VBN" in x ) or ("VBD" in x):
				print("TRUE" + " " + x)
				temp.tense.append("PAST")
			if("will" in x):
				temp.tense.append("FUTURE")

		#mod statement - person

		#self.struct[s] = temp
		

	def define_word(self,key_word,s):
		"""
		Set all the parameters for a word once it is first seen,
		Takes in the word that I want to make the instance of and
		"""
		temp = Words()
		#s = re.sub(r'[^A-Za-z ]','',s)
		temp.word = key_word
		sp = s.split(" ")
		print("The split sentance that the key appears in")
		print(sp)
		index = sp.index(key_word)
		print(index)
		bi = ""
		if(index>=2):
			bi = sp[index-1]+" "+ sp[index]
			print(bi)
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
		#temp.before =  #Dictionaries with the words and their frequencies for both before and after
		#temp.after = 
		temp.word_type = [] #Will be a list because a word can be used in different ways
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

	def generate_trumpism(self):#self,code=0,noise=0):
		"""Different codes will corespond to different topics that could be talked about
			Codes: 0 = Random :: 1 = America :: 2 = China :: 
		"""
		most_used_struct = sorted(self.struct.items(), key = operator.itemgetter(1))
		most_used_words = sorted(self.words_seen.items(),key=operator.itemgetter(1))
		print(self.struct)
		print("This is the most used structs")
		print(most_used_struct)
		trump_string = ""

			

def main():
	test = mimic()
	test.readin()
	test.generate_trumpism()
	
if __name__ == '__main__':
	main()
