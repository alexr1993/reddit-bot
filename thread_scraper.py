## This file is a part of ref bot project

## need to look at writing a corpus tools module, with support for
#  normalising words and manipulating the corpus until it represents a
#  feature vector or something that can easily be transformed into one

import collections
import json
from pprint import pprint
import praw
import re
from start_interactive_shell import start_interactive_shell
from stemming.porter2 import stem
import training_data_finder


global REDDIT
REDDIT = praw.Reddit('alexr1993@gmail.com')

def normalise_word(word):
	'''Processes word so it can be inserted into text corpus'''
	word = re.sub('\W', '', word) # remove non word characters
	word = word.lower()
	#word = stem(word) # don't want to stem if giving to nltk
	return word

def get_thread(url, timelimit=20):
	'''
	Returns list of praw comment objects

	Can be passed an URL to a whole thread, or a specific comment, only
	issue is when given a comment URL only returns the comment, not the
	comment + all its children

	Timelimit in seconds is roughly assured as praw will only send requests
	every 2s, so if the limit is 20 there will be maximum 10 extra requests
	sent.
	'''
	thread = REDDIT.get_submission(url)
	max_calls = int(timelimit / 2)


	if len(thread.comments) == 1:
		print("Fetching children for comment!")

		comment = thread.comments[0]

		print(type(comment))

		thread = training_data_finder.PRAWUtil\
			.get_all_child_comments(comment, max_calls)

	# When it is a single comment (probably meaning a permalink has been)
	# supplied
	else:
		print("Fetching children for submission!")
		## replace_more_comments will replace limit morecomments objects, remove
		# the rest of the morecomments objects and return them from the method
		#
		# Every morecomments that is replaced with take an additional 2s at least
		thread.replace_more_comments(limit=max_calls, threshold=0)
		thread = thread.comments # ditch everything but comments

		print("got comments")

	#for comment in thread:
	#	assert(isinstance(comment, praw.objects.Comment)), type(comment)

	return thread

def normalise_corpus(corpus):
	'''Accepts list of strings. Feeds each word to normalise_word'''
	normalised_corpus = []

	# need to clean up corpus
	for i in range(len(corpus)):
		normalised_corpus.append(normalise_word(corpus[i]))

	return normalised_corpus

def create_corpus(thread):
	'''Accepts list of praw.comments and returns list of words'''
	thread_string = ""

	for comment in thread:
		thread_string += comment.body + ' '

	corpus = thread_string.replace("\n", ' ').split(' ')

	return normalise_corpus(corpus)

def write_corpus_to_file(corpus, path):
	f = open(path, 'w+')

	for word in corpus:
		f.write(word)
		f.write(' ')
	f.close()

## Main
 
# banana for scale urlsf = open('corpus.txt', 'w')

# for word in corpus:
# 	f.write(word)
# 	f.write(' ')

# f.close()
banana1 = 'http://www.reddit.com/r/worldnews/comments/1qluvy/indian_train_strikes_herd_of_40_elephants/cde4vvv'
banana2 = 'http://www.reddit.com/r/pics/comments/1rcx07/caught_a_little_octopus_in_costa_rica/cdm6mj2'
banana3 = 'http://www.reddit.com/r/funny/comments/1reeuf/we_bought_a_big_ass_pizza_today_my_wife_asked_me/'
banana4 = 'http://www.reddit.com/r/funny/comments/1rj8l8/reddit_right_now_fixed/'
banana5 = 'http://www.reddit.com/r/aww/comments/1rkij9/my_girlfriend_works_at_an_animal_shelterso_when/'






banana_for_scale_urls = [banana1, banana2, banana3, banana4, banana5]
banana_for_scale_urls = [banana2]

threads = []

# for url in urls:
# 	print(url)/media/alex/Hitachi
# 	threads += get_thread(url)

front_page = REDDIT.get_front_page()
links = [submission.permalink for submission in front_page]

for submission in banana_for_scale_urls:
	threads.append(get_thread(submission))

corpora = []

# want separate corpus for each thread
for thread in threads:
	corpora.append(create_corpus(thread))

out_folder = '/media/alex/Hitachi/raw_data/banana_for_scale_corpora/'
corpus_id = 1
for corpus in corpora:
	write_corpus_to_file(corpus, out_folder + str(corpus_id) + '.txt')
	corpus_id += 1

	# so I don't spawn 2 million files on my desktop again...
	if corpus_id > 100:
		break


# want a text corpus of everything said in the thread
#master_corpus = create_corpus(threads)



#counter = collections.Counter(master_corpus)

#most_common = counter.most_common(200) # returns n most common, all if none

# sorted set of words, values are the quanitity
#dictionary = dict(counter)

#word_count = sum(dictionary.values())
#vocabulary_size = len(dictionary)

# f = open('corpus.txt', 'w')

# for word in corpus:
# 	f.write(word)
# 	f.write(' ')

# f.close()



#############################################################################
#start_interactive_shell()

import readline # optional, will allow Up/Down/History in the console
import code
vars = globals().copy()
vars.update(locals())
shell = code.InteractiveConsole(vars)
shell.interact()