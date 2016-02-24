import re
import nltk
import sys

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
		self.struct = {}
		self.words_seen = {}
		self.most_prob_noun = []
		self.word_count = 0 #Want to have a general count of every word in the corpus to find the probabilities of certain words.
		self.feature_matrix = []
		self.tense_count = 0
		self.avg_len = 0 #for average length, when updating, keep track of how many structures have been seen, and then multiply average by that then add by the new val and divide by the new total
		

	def readin(self):
		file_name = sys.argv[1]
		"""Read in a file with the with command and then pass it line by line into parse_sentance"""
		with open(file_name) as f:
			for line in f:
				self.parse_sentance(line)

	def parse_sentance(self,s):
		#Create the dictionary of Words with their respective parts of speech
		sentance = s
		tokens =  nltk.word_tokenize(sentance)
		pos = nltk.pos_tag(tokens)
		store_sentance = "" #Stores the structure of the sentance
		#Key is the word and val is its grammaical identification
		for key,val in pos:
			store_sentance += val + "-"
			print(key + " :: " + val)
			if key in self.words_seen:
				temp = self.words_seen[key]
				self.words_seen[key] = temp+1


			else:
				self.words_seen[key] = 1
				word_only = re.sub(r'[^A-Za-z ]','',sentance)
				if(key.isalpha()):
					print("Reach this statement")
					self.define_word(key,word_only)
				# -- will go here when the word is first seen and fill out all its
		print(store_sentance)
		print(self.words_seen)
		#need to implement an if statement to see if the grammer struct has been seen before, though much more unlikely than words, it is still possible
		if (store_sentance in self.struct):
			pass
		else:
			self.define_grammer(store_sentance)
		print(self.struct)
	
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

		self.struct[s] = temp
		pass

	def define_word(self,w,s):
		"""
		Set all the parameters for a word once it is first seen,
		Takes in the word that I want to make the instance of and
		"""
		temp = Words()
		#s = re.sub(r'[^A-Za-z ]','',s)
		temp.word = w
		sp = s.split(" ")
		print(sp)
		index = sp.index(w)
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
			temp[before] = 0
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
		#I see a subjective word and naively add or subtract, next four steps will change this approach so its not so naive.
			ind = s.index(i)
			if (s in pos_lex):
				pos_val += 1
			if (s in neg_lex):
				neg_val += -1
		#Negations -- if there is a negation (no,not,etc) and is followed by a subjective word, will look at last 4 words
			if(index-4 < 0):

		#modifiers -- presence of words like very, super, extremely
		
		#Polarity shift -- Expressing and opinion (pos/neg) then flip

		#Subject opinion -- how does the speaker feel about the subject and nouns in the current sentance, this will be pulled from the dict
		
		

		return val

		def generate_trumpism():
			pass

def main():
	test = mimic()
	test.readin()
	test.construct_vector()
	
if __name__ == '__main__':
	main()
