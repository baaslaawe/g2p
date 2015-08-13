import sys
import os


""" This file maps the manual transliterations into phonemes using
automatic transliterations and mono-phoneset file. First step is to
find the one-to-one mapping between mannual and automatic 
tranliterations. There could be mismatches between them, i.e.
sometimes people may mix two words into single or they forget to 
transliterate some words. This tries to correct one word mistakes.

"""

###############################
# After careful observation, we find this table which shows the
# possible phonemes for each grapheme. We can see that, at least for
# telugu, people didn't use the letters 'q', and 'w' for transliteration

ph_dic = {}
ph_dic['2'] = ['r']
ph_dic['3'] = ['t', 'm']
ph_dic['a'] = ['aa', 'ai', 'e', 'ei']
ph_dic['b'] = ['bh']
ph_dic['c'] = ['ch', 'k', 's']
ph_dic['d'] = ['dh', 'dx', 'dxh']
ph_dic['e'] = ['ai', 'ei', 'i', 'ii']
ph_dic['f'] = ['ph']
ph_dic['g'] = ['gh', 'j']
ph_dic['h'] = ['h']
ph_dic['i'] = ['a', 'ai', 'ii']
ph_dic['j'] = ['j']
ph_dic['k'] = ['c', 'kh']
ph_dic['l'] = ['e']
ph_dic['m'] = ['e']
ph_dic['n'] = ['e']
ph_dic['o'] = ['aa', 'a', 'au', 'oo', 'uu', 'w']
ph_dic['p'] = ['ph']
ph_dic['r'] = ['aa', 'rq', 'w']
ph_dic['s'] = ['e', 'sh', 'sx']
ph_dic['t'] = ['dh', 'th', 'tx', 'txh']
ph_dic['u'] = ['a','uu', 'w', 'y']
ph_dic['v'] = ['ei','u','uu', 'w']
ph_dic['x'] = ['e']
ph_dic['y'] = ['e', 'ei', 'w']
ph_dic['z'] = ['j']
####################################

# convert each word into corresponding phoneme representation
def word2phone(phoneset, word):
	# phoneset contains the list of monophones
	# split the word into small subwords and check they are equal to any phone
	# in the phonelist
	j = 0
	phones = []
	while j < len(word):
		# check if three letters of a word are equal to a phone or not
		if word[j:j+3] in phoneset:
			phones.append(word[j:j+3])
			j = j + 3
		# check if two letters of a word are equal to a phone or not
		elif word[j:j+2] in phoneset:
			phones.append(word[j:j+2])
			j = j + 2
		else:
			# else if we check single letter of a word is in the phoneset
			# most/all of the cases single letter will have a correspond phone
			if word[j] in phoneset:
				phones.append(word[j])
				j = j + 1
	return phones


# this function modifys the single word mistakes by joining the two words in the
# longer list
def adjust_oneword_mistakes(a, t):
	flag = 0
	if len(t) > len(a):
		for j in xrange(len(t)):
			if j == len(a):
				t[j-1] = t[j - 1] + t[j]
				t.pop(j)
				break
			else:
				if (a[j][0] != t[j][0]) and (t[j][0] not in ph_dic[a[j][0]]):
					t[j-1] = t[j-1] + t[j]
					t.pop(j)
					break
		return a, t
	else:
		for j in xrange(len(a)):
			if j == len(t):
				a[j-1] = a[j - 1] + a[j]
				a.pop(j)
				break
			else:
				if (a[j][0] != t[j][0]) and (t[j][0] not in ph_dic[a[j][0]]):
					a[j-1] = a[j-1] + a[j]
					a.pop(j)
					break
		return a, t

if __name__ == "__main__":

	if len(sys.argv) != 4:
		sys.exit("Usage: python text_to_phone.py <manual transliteration file> \
			      <automatic tranliteration file> <mono-phoneset file>")

	# get mannual transliteration/annotation file 
	annont_file = sys.argv[1]
	# get automatic transliteration file
	trans_file = sys.argv[2]
	# get mono-phones file
	lang_file = sys.argv[3]

	### Read mono-phones into a list ###
	phoneset = [] # initialize the phoneset
	# open the phoneset file which contains utf8 and their correspond phone
	with open(lang_file, 'r') as f:
		for line in f.readlines():
			ph_list = line.strip().split()
			if ph_list[1] not in phoneset:
				phoneset.append(ph_list[1])

	### Read annotation file ####
	with open(annont_file, 'r') as f:
		annont_lines = f.readlines()

	### Read transliteration file ###
	with open(trans_file, 'r') as f:
		trans_lines = f.readlines()

	### sanity check ###
	if len(annont_lines) != len(trans_lines):
		sys.exit('The number of lines in automatic and mannual transliteration \
			files are different. Check agian!')

	### Convert each sentence into its phonemic representation ###
	w2p_train = []
	train_dic = {}
	test_words = []

	for i in xrange(len(annont_lines)):
		# the lines in these ranges are for test set, thus just add them to test set
		if (i >= 1850 and i <= 1900) or (i >= 2200):
			a_list = annont_lines[i].strip().split()
			for w in a_list:
				if w not in test_words:
					test_words.append(w)
			continue

		a_list = annont_lines[i].strip().split()
		t_list = trans_lines[i].strip().split()
		a_len = len(a_list)
		t_len = len(t_list)

		# As of now we care about only one word mistakes!
		if abs(a_len - t_len) <= 1:
			# if the lengths difference is one then adjust the bigger list by merging
			# two words	
			if abs(a_len - t_len) == 1:
				#print "before", a_list, t_list
				a_list, t_list = adjust_oneword_mistakes(a_list, t_list)
				#print "after", a_list, t_list

			for j in xrange(len(a_list)):
				# check that current word is unique or not
				if a_list[j] not in train_dic:
					# map the word to phone
					phones = word2phone(phoneset, t_list[j])
					# add the word into dictionary
					train_dic[a_list[j]] = ' '.join(phones)
					# this is double check to make sure that phones are correspond
					# to the annotation word by comparing the first phone in both
					# word and phones
					if a_list[j][0] == phones[0] or phones[0] in ph_dic[a_list[j][0]]:
						w2p_train.append(a_list[j] + ' ' + ' '.join(phones))


	with open('lexicon_train.txt', 'w') as f:
		f.write('\n'.join(w2p_train))
	with open('test.words', 'w') as f:
		f.write('\n'.join(test_words))

	os.system('cat lexicon_train.txt | sort | uniq > temp.txt')
	os.system('rm lexicon_train.txt')
	os.system('mv temp.txt train.lex')
